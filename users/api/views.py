from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.authentication import CSRFCheck
from users.api.serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, OrderSerializer, ProfileSerializer
from users.models import User, Address, Order, Profile
from django.http import JsonResponse
import requests
from django.conf import settings
from rest_framework import permissions
from users.api.serializers import UserSerializer, UserAddressSerializer, SocialLoginSerializer

from allauth.socialaccount.models import SocialAccount
# from dj_rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from allauth.socialaccount.providers.kakao import views as kakao_view

# Create your views here.
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        
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

REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
class UserAddressAPIView(generics.ListAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자에게만 접근 권한 부여

    def get(self, request, *args, **kwargs):
        address = "서울시 동대문구 이문동"
        if not address:
            return Response({'error': '주소를 제공해야 합니다.'}, status=400)
        
        url = f'https://apis.daum.net/local/geo/addr2coord?apikey={REST_API_KEY}&q={address}&output=json'
        headers = {"Authorization": "KakaoAK {}".format(REST_API_KEY)}
        params = {"query": "{}".format(address)}
        
        resp = requests.get(url, params=params, headers=headers)
        documents = resp.json().get("documents", [])
        
        return Response(documents)
    
    def post(self, request, *args, **kwargs):
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        headers = {"Authorization": "KakaoAK {}".format(REST_API_KEY)}
        address = "서울시 동대문구 이문동"
        params = {"query": "{}".format(address)}
        resp = requests.get(url, params=params, headers=headers)
        documents = resp.json()["documents"]

        first_documents = documents
        address_instance = Address.objects.create(
            user = request.user,
            zonecode = first_documents.get("zonecode"),
            roadAddress = first_documents.get("road_address"),
            buildingName = first_documents.get("building_name"),
            sigungu = first_documents.get("sigungu"),
            latitude = first_documents.get('y'),
            longitude = first_documents.get('x'),
        )
        serializer = UserAddressSerializer(address_instance)
        return Response(serializer.data)


class UserOrderAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id)

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
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    """
    get:
        Returns a list of all existing posts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
