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