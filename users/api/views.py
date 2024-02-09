from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from rest_framework.renderers import JSONRenderer
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.authentication import CSRFCheck
from users.api.serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, AddressSerializer, OrderSerializer
from users.models import User, Address, Order
from django.http import JsonResponse
import requests
from django.contrib import messages
from json.decoder import JSONDecodeError
from urllib.parse import urlparse
from django.conf import settings

from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.kakao import views as kakao_view

# Create your views here.
##### 시리얼라이저를 사용해서 유저를 저장하고(=회원가입), JWT토큰을 발급받아 쿠키에 저장한다.
##### 쿠키에 저장할 떄, `httpOnly=True` 속성을 지정 → Javascript로부터 쿠키를 조회할 수 없도록
##### XSS로부터 안전하지만 CSRF문제가 발생 → CSRF 부분 보완
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        
            ##### JWT 토큰 접근
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

            ##### JWT 토큰 쿠키에 저장
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
    
    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

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
    
class UserAddressAPIView(generics.ListAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Address.objects.filter(user_id=user_id)
    
    def KaKaoAPIView(address):
        address = "서울시 강남구 도곡동"    
    
        url = f"https://dapi.kakao.com/v2/local/search/address.json?query={address}"
        results = requests.get(urlparse(url).geturl(), headers={"Authorization" : "KakaoAK 3086e0fa06801c242f3f6d1ca5ab6bef"}).json()

        lat = results["documents"][0]["x"]
        lng = results["documents"][0]["y"]
        crd = {"lat": str(lat), "lng": str(lng)}
        return JsonResponse(crd, status=201)

class UserOrderAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id)

##### 카카오 로그인창을 띄우고, 사용자가 카카오 계정으로 로그인을 하면 인증 코드를 받아오는 함수
##### 토큰 받기
##### 토큰을 기반으로 사용자 로그인 처리
class GetKakaoAccessView(APIView):
    def post(self, request, *args, **kwargs):
        kakao_access_token = request.data.get("access_token")
        ##### Profile request
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {kakao_access_token}"})
        profile_json = profile_request.json()
        kakao_account = profile_json.get('kakao_account')
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
    def post(self, request, *args, **kwargs):
        google_access_token = request.data.get("access_token")
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