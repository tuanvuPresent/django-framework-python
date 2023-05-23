from apps.account.models import User
from rest_framework import serializers

from .tasks import send_mail_reset_password_v3
from ..utils import CustomPasswordResetTokenGenerator
from ....common.constant import ErrorMessage
from ....common.custom_exception_handler import CustomAPIException


class ResetPasswordSerializer3(serializers.Serializer):
    email = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if not email or email == "":
            raise CustomAPIException(ErrorMessage.EMAIL_REQUIRED)
        if not user:
            raise CustomAPIException(ErrorMessage.EMAIL_NOT_EXIST)

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
            raise CustomAPIException(ErrorMessage.TOKEN_REQUIRED)
        if not uid or uid == "":
            raise CustomAPIException(ErrorMessage.UID_REQUIRED)
        uid = CustomPasswordResetTokenGenerator().decode_uid(uid)
        user = User.objects.filter(id=uid).first()
        if not CustomPasswordResetTokenGenerator().check_token(user, token):
            raise CustomAPIException(ErrorMessage.LINK_RESET_PASS_INVALID)
        attrs['user'] = user
        return attrs


class ResetPasswordCompleteSerializer3(CheckResetPasswordSerializer3):
    new_password = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        new_password = attrs.get('new_password')
        if not new_password or new_password == "":
            raise CustomAPIException(ErrorMessage.PASSWORD_REQUIRED)

        user = attrs.get('user')
        user.set_password(new_password)
        user.save()
        return attrs
