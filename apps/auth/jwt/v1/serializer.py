from datetime import datetime

from django.contrib.auth import authenticate
from jwt import ExpiredSignatureError, DecodeError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.settings import api_settings

from apps.account.models import User
from ..utils import CustomEmailVerifyTokenGenerator, CustomPasswordResetTokenGenerator
from apps.common.jwt_handle import JwtRefreshTokenGenerator
from ...jwt.v1.tasks import send_mail_reset_password
from ....common.constant import ErrorMessage
from ....common.custom_exception_handler import CustomAPIException


class JWTLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64, required=True)
    password = serializers.CharField(max_length=64, required=True, help_text='Leave empty if no change needed',
                                     style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username or not password:
            raise serializers.ValidationError('password and username field required')

        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed()
        return user


class JWTAdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64, required=True)
    password = serializers.CharField(max_length=64, required=True, help_text='Leave empty if no change needed',
                                     style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username or not password:
            raise serializers.ValidationError('password and username field required')

        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed()
        if not user.is_admin:
            raise AuthenticationFailed()
        return user


class JWTRefreshTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=512)

    def validate(self, attrs):
        token = attrs.get('token')
        try:
            token_generator = JwtRefreshTokenGenerator()
            payload = token_generator.verify_refresh_token(token)
        except ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired!')
        except DecodeError:
            raise AuthenticationFailed('Invalid Token!')
        except Exception:
            raise AuthenticationFailed('Invalid token.')


        user = User.objects.filter(pk=token_generator.user_id).first()
        if not user:
            raise AuthenticationFailed('No user matching this token was found.')

        return {
            'user': user,
            'token': JwtRefreshTokenGenerator().get_token(user)
        }


class JWTPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32, required=True)
    new_password = serializers.CharField(max_length=32, required=True)
    verified_password = serializers.CharField(max_length=32, required=True)

    def validate(self, data):
        password = data.get('password', None)
        new_password = data.get('new_password', None)
        verified_password = data.get('verified_password', None)

        user = self.context.get('request').user
        if not user.check_password(password):
            raise CustomAPIException('Your current password is incorrect.')

        if new_password != verified_password:
            raise CustomAPIException('Your passwords didnt match.')

        return data

    def create(self, validated_data):
        new_password = validated_data.get('new_password', None)

        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()
        return validated_data


class JWTPasswordResetSerializer(serializers.Serializer):
    username = serializers.EmailField(max_length=32, required=True)

    def validate(self, data):
        username = data.get('username', None)
        user = User.objects.filter(email=username).first()
        if not user:
            raise serializers.ValidationError('username is not exists')
        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data.get('user')
        new_password = user.make_random_password()
        user.set_password(new_password)
        user.save()

        send_mail_reset_password.delay(user.email, new_password)

        return validated_data


class SocialLoginSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)
