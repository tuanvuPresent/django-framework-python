from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from apps.common.custom_exception_handler import CustomAPIException
from apps.my_phone_verify.service import PhoneVerificationService


class PhoneRegisterSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()


class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    session_token = serializers.CharField(required=True)
    security_code = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        phone_number = attrs.get("phone_number", None)
        security_code = attrs.get("security_code", None)
        session_token = attrs.get("session_token", None)

        phone_verification_service = PhoneVerificationService()
        verification = phone_verification_service.validate_security_code(
            security_code, phone_number, session_token
        )

        if verification == phone_verification_service.SECURITY_CODE_INVALID:
            raise CustomAPIException('Security code is not valid')
        elif verification == phone_verification_service.SESSION_TOKEN_INVALID:
            raise CustomAPIException('Session token is not valid')
        elif verification == phone_verification_service.SECURITY_CODE_EXPIRED:
            raise CustomAPIException('Security code has expired')
        elif verification == phone_verification_service.SECURITY_CODE_VERIFIED:
            raise CustomAPIException('Security code is already verified')

        return attrs
