from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.custom_model_view_set import BaseGenericViewSet
from apps.my_phone_verify.models import Phone
from apps.my_phone_verify.serializer import PhoneRegisterSerializer, PhoneVerificationSerializer
from apps.my_phone_verify.service import PhoneVerificationService


class VerificationPhoneView(BaseGenericViewSet):
    serializer_action_classes = {
        'register': PhoneRegisterSerializer,
        'verify': PhoneVerificationSerializer
    }

    @action(methods=['POST'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        phone_number = request.data.get('phone_number')
        serializer.is_valid(raise_exception=True)

        phone_verification_service = PhoneVerificationService()
        security_code = phone_verification_service.generate_security_code()
        token = phone_verification_service.generate_session_token(phone_number)
        phone_verification_service.send_security_code(
            message=f'use session code {security_code} for authentication.',
            to=phone_number,
        )
        Phone.objects.filter(phone_number=phone_number).delete()
        Phone.objects.create(
            phone_number=phone_number,
            security_code=security_code,
            session_token=token
        )
        return Response(data={'token': token})

    @action(methods=['POST'], detail=False)
    def verify(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=None)
