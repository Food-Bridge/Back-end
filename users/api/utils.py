import jwt
import requests
from urllib.parse import urlparse
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

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
    
def geocode_address(address):
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
                    return {
                        'latitude': 0,
                        'longitude': 0,
                    }
        except requests.exceptions.RequestException as e:
            raise Response({'error': f"Error during geocoding: {e}"}, status=status.HTTP_400_BAD_REQUEST)