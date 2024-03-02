import jwt
from django.conf import settings
from coupon.models import Coupon
from users_coupon.models import UserCoupon
from rest_framework.exceptions import AuthenticationFailed

def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def decode_access_token(access_token):
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired, please log in again')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token, please log in again')

def register_coupon_to_user(user):
    register_coupon_ids = [7, 8, 9]
    for coupon_id in register_coupon_ids:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            UserCoupon.objects.create(user=user, coupon=coupon)
        except Coupon.DoesNotExist:
            pass  # 쿠폰이 존재하지 않는 경우 아무 작업도 수행하지 않음