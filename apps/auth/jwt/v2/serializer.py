from datetime import datetime

from django.contrib.auth import authenticate
from jwt import ExpiredSignatureError, DecodeError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.settings import api_settings

from apps.account.models import User
from ..utils import CustomEmailVerifyTokenGenerator, CustomPasswordResetTokenGenerator
from ....common.jwt_handle import jwt_decode_handler, jwt_payload_handler, jwt_encode_handler
from .tasks import send_mail_reset_password_v2
from ....common.constant import ErrorCode
from ....common.custom_exception_handler import CustomAPIException


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

