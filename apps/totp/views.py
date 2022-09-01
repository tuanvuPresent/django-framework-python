from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_pyotp.serializers import NoneSerializer

from apps.totp.models import UserOtpDevice
from apps.totp.serializers import TOTPProvisionUriSerializer, VerifyOtpSerilaizer


class AuthOtpViewSet(viewsets.GenericViewSet):
    queryset = UserOtpDevice.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'generate_totp_provision_uri':
            return TOTPProvisionUriSerializer
        if self.action == 'verify_otp':
            return VerifyOtpSerilaizer
        return NoneSerializer

    @action(methods=['POST'], detail=False, url_path='generate-totp/provision-uri')
    def generate_totp_provision_uri(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = serializer.save()

        return Response({
            'uri': res
        }, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, url_path='verify')
    def verify_otp(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK)
