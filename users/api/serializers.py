from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.contrib import auth
from django.conf import settings

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

from users.api.utils import generate_access_token, decode_access_token
from users.models import User, Address, Profile
from restaurant.models import Restaurant

from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3, required=True)
    password = serializers.CharField(max_length=68, min_length=6, required=True, write_only=True)
    password2= serializers.CharField(required=True, write_only=True)
    phone_number = PhoneNumberField(help_text='휴대폰 번호', region='KR')
    username = serializers.CharField(
        max_length=150,
        min_length=3,
        required=True,
        validators=[UnicodeUsernameValidator()],
    )
    is_seller = serializers.BooleanField(default=False)

    class Meta:
        model   = User
        fields  = ['email', 'username', 'password', 'password2', 'phone_number', 'is_seller',]
    
    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        password2 = attrs.pop('password2', '')
        email = attrs.get('email', '')

        ph_number   = attrs.get('phone_number', '')
        phone_number= phonenumbers.parse(ph_number, 'KR')
        
        if password != password2:
            raise serializers.ValidationError({"password":"Password and Confirm Password Does not match"})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"message": "This username is already taken with the same email."})    
        
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            is_seller=validated_data['is_seller'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()
    is_seller = serializers.BooleanField(required=True)
    owner = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
        
    def get_owner(self, obj):
        user = User.objects.get(email=obj['email'])
        restaurants = Restaurant.objects.filter(owner=user) # 매장 찾기
        return [restaurant.id for restaurant in restaurants] # 여러 매장을 가질 수 있다고 가정
    
    class Meta:
        model = User
        fields = ['password', 'email', 'tokens', 'is_seller', 'owner']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)  # authenticate에서 email 사용
        
        if not user:
            raise serializers.ValidationError({'message' : 'User does not exist. try again'})
        if not user.is_active:
            raise serializers.ValidationError({'message' : 'Account disabled, contact admin'})
        
        validated_user = User.objects.get(email=email)
        is_seller = validated_user.is_seller
        if is_seller != attrs.get('is_seller'):
            raise serializers.ValidationError({'message' : '사용자 정보가 올바르지 않습니다.'})

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens,
            'is_seller' : user.is_seller,
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs.get('refresh')
        
        if not self.token:
            raise ValidationError({'message' : "Token value is empty."})
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.verify()
        except TokenError as e:
            raise ValidationError({'message': e})
        return attrs
    def save(self):
        RefreshToken(self.token).blacklist()

class AddressSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    class Meta:
        model = Address
        fields = ['user', 'id', 'nickname', 'detail_address', 'road_address', 'jibun_address', 'building_name', 'sigungu', 'is_default', 'full_address',]

##### 전체 사용자 정보를 조회(주소 정보 처리 확인 차원)
class UserSerializer(serializers.ModelSerializer):
    # address = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username',)

class SocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Profile
        fields = ['user', 'nickname', 'image']
        
    def create(self, validated_data):
        instance = Profile.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            ext = str(image_data).split('.')[-1] # ext에 확장자 명이 담긴다.
            ext = ext.lower() # 확장자를 소문자로 통일
            if ext in ['jpg', 'jpeg','png',]:
                Profile.objects.create(article=instance, image=image_data, image_original=image_data)
            elif ext in ['gif','webp']:
                Profile.objects.create(article=instance, image_original=image_data)
        return instance
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 이미지가 없는 경우에는 image_original 값을 반환
        if not ret['image']:
            ret['image'] = self.context['request'].build_absolute_uri(settings.MEDIA_URL + str(instance.image_original))
        return ret