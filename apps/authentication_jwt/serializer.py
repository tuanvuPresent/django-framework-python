from datetime import datetime

from django.contrib.auth import authenticate
from jwt import ExpiredSignatureError, DecodeError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.settings import api_settings

from apps.account.models import User
from .utils.email_verify import CustomEmailVerifyTokenGenerator, CustomPasswordResetTokenGenerator
from .utils.jwt_handle import jwt_decode_handler, jwt_payload_handler, jwt_encode_handler
from .utils.send_mail_handle import send_mail_reset_password, send_mail_reset_password_v2, send_mail_reset_password_v3
from ..common.constant import ErrorCode
from ..common.custom_exception_handler import CustomAPIException


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
            payload = jwt_decode_handler(token)
        except ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired!')
        except DecodeError:
            raise AuthenticationFailed('Invalid Token!')
        except Exception:
            raise AuthenticationFailed('Invalid token.')

        try:
            user = User.objects.get(pk=payload.get('user_id'))
        except User.DoesNotExist:
            raise AuthenticationFailed('No user matching this token was found.')

        orig_iat = payload.get('orig_iat')
        if api_settings.JWT_ALLOW_REFRESH:
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA.total_seconds()

            expiration_timestamp = orig_iat + int(refresh_limit)
            now_timestamp = datetime.now().astimezone().timestamp()
            if now_timestamp > expiration_timestamp:
                raise CustomAPIException('Refresh has expired.')
        else:
            raise CustomAPIException('Not allow refresh.')

        new_payload = jwt_payload_handler(user)
        new_payload['orig_iat'] = orig_iat
        return {
            'user': user,
            'token': jwt_encode_handler(new_payload)
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


class ResetPasswordSerializer2(serializers.Serializer):
    email = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        email = attrs.get('email')
        token_generator = CustomEmailVerifyTokenGenerator()
        user = User.objects.filter(email=email).first()
        if not email or email == "":
            raise CustomAPIException(ErrorCode.EMAIL_REQUIRED)
        if not user:
            raise CustomAPIException(ErrorCode.EMAIL_NOT_EXIST)

        time_token = datetime.now().timestamp()
        code = token_generator.make_code(user, time_token)
        token = token_generator.make_token(user, time_token)
        send_mail_reset_password_v2(to_email=email, code=code)
        return token


class ResetPasswordCompleteSerializer(serializers.Serializer):
    session_token = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)
    new_password = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        session_token = attrs.get('session_token')
        code = attrs.get('code')
        new_password = attrs.get('new_password')

        if not code or code == "":
            raise CustomAPIException(ErrorCode.RESET_PASSWORD_CODE_REQUIRED)
        if not new_password or new_password == "":
            raise CustomAPIException(ErrorCode.PASSWORD_REQUIRED)

        token_generator = CustomEmailVerifyTokenGenerator()
        is_valid, user = token_generator.check_token(session_token)
        if not is_valid:
            raise CustomAPIException(ErrorCode.RESET_PASSWORD_TOKEN_INVALID)
        if not token_generator.check_code(user=user, code=code):
            raise CustomAPIException(ErrorCode.RESET_PASSWORD_CODE_INVALID)
        return {'user': user, 'new_password': attrs.get('new_password')}


class ResetPasswordSerializer3(serializers.Serializer):
    email = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if not email or email == "":
            raise CustomAPIException(ErrorCode.EMAIL_REQUIRED)
        if not user:
            raise CustomAPIException(ErrorCode.EMAIL_NOT_EXIST)

        token = CustomPasswordResetTokenGenerator().make_token(user)
        uid = CustomPasswordResetTokenGenerator().make_uid(user)
        send_mail_reset_password_v3(email, uid, token)
        return attrs


class CheckResetPasswordSerializer3(serializers.Serializer):
    token = serializers.CharField(required=False, allow_blank=True)
    uid = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        token = attrs.get('token')
        uid = attrs.get('uid')
        if not token or token == "":
            raise CustomAPIException(ErrorCode.TOKEN_REQUIRED)
        if not uid or uid == "":
            raise CustomAPIException(ErrorCode.UID_REQUIRED)
        uid = CustomPasswordResetTokenGenerator().decode_uid(uid)
        user = User.objects.filter(id=uid).first()
        if not CustomPasswordResetTokenGenerator().check_token(user, token):
            raise CustomAPIException(ErrorCode.LINK_RESET_PASS_INVALID)
        attrs['user'] = user
        return attrs


class ResetPasswordCompleteSerializer3(CheckResetPasswordSerializer3):
    new_password = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        new_password = attrs.get('new_password')
        if not new_password or new_password == "":
            raise CustomAPIException(ErrorCode.PASSWORD_REQUIRED)

        user = attrs.get('user')
        user.set_password(new_password)
        user.save()
        return attrs
