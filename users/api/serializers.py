from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from django.contrib import auth
from django.conf import settings

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError

from users.api.utils import generate_access_token, decode_access_token
from users.models import User, Address, Order, Profile

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

    class Meta:
        model   = User
        fields  = ['email', 'username', 'password', 'password2', 'phone_number', 'is_seller']
    
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
            is_seller=validated_data['is_seller']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['password', 'email', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)  # authenticate에서 email 사용
        if not user:
            raise AuthenticationFailed({'message' : 'User does not exist. try again'})
        if not user.is_active:
            raise AuthenticationFailed({'message' : 'Account disabled, contact admin'})
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
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
        fields = ['user', 'id', 'nickname', 'detail_address', 'road_address', 'jibun_address', 'building_name', 'sigungu', 'is_default' ]

class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"

class SocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_id', 'nickname', 'image']
        
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