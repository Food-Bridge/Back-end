from django.urls import path
from users.api.views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    OnlyAuthenticatiedUserView,
    UserAddressAPIView,
    UserOrderAPIView,
    GetKakaoAccessView,
    GetGoogleAccessView,
    ProfileView
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Access Token, Refresh Token 
# Logic1. 요청을 보내자마자 액세스 토큰 형식으로 응답을 받고 새로고침된다.
# Logic2. 액세스 토큰의 한계 : 기본적으로 5분 동안만 지속된다는 문제가 발생 → 5분이 지나면 자동 폐기
# Logic3. 액세스 토큰이 파괴되면 이를 다시 생성하기 위해 새로고침 토큰을 사용
# Logic4. 새로고침 토큰은 기본적으로 24시간동안 유효함
# Logic5. 이러한 토큰이 자동적으로 저장되고 생성되지 않는다.
# Logic6. 클라이언트 측에서 액세스 토큰과 새로고침 토큰 두 가지를 로컬 스토리지에 저장
# Logic7. 로컬 스토리지에 가지고 다니는데 액세스 토큰은 5분, 새로고침 토큰은 24시간
# Login8. token/refresh/에 리프레시 토큰 값을 가지고 호출하면 갱신된 액세스 토큰을 재발급 받음

urlpatterns = [
    ##### 로그인, 로그아웃, 회원가입
    path('signup/', RegisterAPIView.as_view(),name="signup"),
    path('login/', LoginAPIView.as_view(),name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),

    ##### 회원별 주소
    path('<int:user_id>/address/', UserAddressAPIView.as_view(), name="address"),
    
    ##### 회원별 주문 내역
    path('<int:user_id>/orders/', UserOrderAPIView.as_view(), name="orders"),
    
    ##### 회원 프로파일
    path('profile/', ProfileView.as_view(), name="profile"),

    path('authonly/', OnlyAuthenticatiedUserView.as_view(), name="authonly"),
    
    ##### 카카오 소셜 로그인
    path('kakao/login/callback/', GetKakaoAccessView.as_view(), name="kakao_callback"),
    # 구글 소셜로그인 콜백(로그인/회원가입)
    path('google/login/callback/', GetGoogleAccessView.as_view(), name='google_callback'),
]