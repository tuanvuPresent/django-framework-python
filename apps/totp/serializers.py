from rest_framework import serializers

from api.totp.utils import TotpService


class TOTPProvisionUriSerializer(serializers.Serializer):
    time = serializers.IntegerField(required=False, default=30)

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        time = validated_data.pop('time')

        return TotpService(step=time).provisioning_uri(user_id=user_id)


class VerifyOtpSerilaizer(serializers.Serializer):
    otp = serializers.CharField()

    def validate(self, attrs):
        request = self.context.get('request')
        user_id = request.user.id
        otp = attrs.get('otp')

        is_valid = TotpService().verify(user_id=user_id, otp=otp)
        if not is_valid:
            raise serializers.ValidationError('OTP không hợp lệ')

        return True
