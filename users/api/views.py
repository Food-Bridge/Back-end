import requests
from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.authentication import CSRFCheck
from users.models import User, Address, Profile
from coupon.models import Coupon
from users_coupon.models import UserCoupon
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from urllib.parse import urlparse
from users.api.serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProfileSerializer,
    AddressSerializer,
    SocialLoginSerializer,
    UserSerializer
    )
from allauth.socialaccount.models import SocialAccount

class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            coupon, created = Coupon.objects.get_or_create(code='회원가입 축하 쿠폰')
            UserCoupon.objects.create(user=user, coupon=coupon)

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user" : serializer.data,
                    "message" : "회원가입이 완료되었습니다.",
                    "token" : {
                        "access" : access_token,
                        "refresh" : refresh_token,
                    },
                },
                status = status.HTTP_200_OK,
            )

            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def enforce_csrf(self, request, *args, **kwargs):
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OnlyAuthenticatiedUserView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        if not user:
            return Response({"error" : "접근 권한이 없다."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message" : "Accepted"})
    
class UserAddressAPIView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Address.objects.filter(user_id=user_id)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        data['user_id'] = self.request.user.id
        data['full_address'] = f"{data['road_address']} {data['detail_address']}"

        if 'detail_address' in data:
            try:
                address = data['detail_address']
                geocoded_data = self.geocode_address(address)
                if geocoded_data:
                    data.update(geocoded_data)
            except requests.exceptions.RequestException as e:
                return Response({'error': f"Error during geocoding: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(**data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def geocode_address(self, address):
        KAKAO_REST_API_KEY = getattr(settings, 'KAKAO_REST_API_KEY')
        url = f"https://dapi.kakao.com/v2/local/search/address.json?query={address}"
        
        try:
            response = requests.get(urlparse(url).geturl(), headers={"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"})
            if response.status_code == 200:
                result = response.json()
                documents = result.get('documents', [])
                if documents:
                    return {
                        'latitude': float(documents[0]['y']),
                        'longitude': float(documents[0]['x']),
                    }
            else:
                return Response({'error': f"Error during geocoding: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as e:
            raise Response({'error': f"Error during geocoding: {e}"}, status=status.HTTP_400_BAD_REQUEST)

class UserAddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.request.user.id
        obj_id = self.kwargs.get('pk')
        queryset = Address.objects.filter(user_id=user_id, id=obj_id)
        return queryset
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        
        user_id = self.request.user.id
        obj_id = self.kwargs.get('pk')
        
        instance = get_object_or_404(Address, user_id=user_id, id=obj_id)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        instance.is_default = not instance.is_default
        instance.save()
        return Response({'is_default': instance.is_default}, status=status.HTTP_200_OK)


class GetKakaoAccessView(APIView):
    serializer_class = SocialLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = SocialLoginSerializer(data=request.data)
        if serializer.is_valid():
            kakao_access_token = serializer.validated_data.get("access_token")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ##### Profile request
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {kakao_access_token}"})
        profile_json = profile_request.json()
        kakao_account = profile_json.get('kakao_account')
        
        if kakao_account is None:
            return Response("err_msg : failed to get email", status=status.HTTP_400_BAD_REQUEST)
        
        ##### Email
        email = kakao_account.get('email')
        try:
            user = User.objects.get(email=email)
            message = "카카오 소셜 로그인 완료"
        except User.DoesNotExist:
            user = User.objects.create(email=email)
            message = "회원가입 완료"

        ##### jwt 토큰
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        res = Response(
            {
                "user" : email,
                "message" : message,
                "token" : {
                    "access" : access_token,
                    "refresh" : refresh_token,
                },
            },
            status = status.HTTP_200_OK,
        )
        res.renderer_context = {}
        res.accepted_renderer = JSONRenderer()
        res.accepted_media_type = "application/json"
        ##### JWT 토큰 쿠키에 저장
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)
        return res
    
class GetGoogleAccessView(APIView):
    serializer_class = SocialLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = SocialLoginSerializer(data=request.data)
        if serializer.is_valid():
            google_access_token = serializer.validated_data.get("access_token")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={google_access_token}")
        email_req_status = email_req.status_code
        
        if email_req_status != 200:
            return Response({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
        email_req_json = email_req.json()
        email = email_req_json.get('email')
        
        try:
            user = User.objects.get(email=email)
            message = "구글 소셜 로그인이 완료되었습니다."
        except User.DoesNotExist:
            user = User.objects.create(email=email)
            message = "구글 소셜 회원가입이 완료되었습니다."
        except SocialAccount.DoesNotExist:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        
        res = Response({
            "user": email,
            "message": message,
            "token": {
                "access": access_token,
                "refresh": refresh_token
            }
        }, status=status.HTTP_200_OK)
        
        return res

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
    def get_object(self):
        # JWT 토큰에서 사용자 ID를 가져옴
        user_id = self.request.user.id
        # 해당 사용자 ID에 해당하는 프로필을 가져옴
        profile = Profile.objects.get(user_id=user_id)
        return profile

    def get(self, request, *args, **kwargs):
        # GET 요청을 처리하여 사용자의 프로필을 반환
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # PUT 요청을 처리하여 사용자의 프로필을 업데이트
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserInfoAPIView(generics.ListAPIView):
    """
    get:
        Returns a list of all existing posts
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()