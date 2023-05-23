from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.auth.jwt.v3.serializer import ResetPasswordSerializer3, \
    ResetPasswordCompleteSerializer3, CheckResetPasswordSerializer3
from apps.common.custom_model_view_set import BaseGenericViewSet


class JWTAuthAPIView(BaseGenericViewSet):
    serializer_action_classes = {
        'reset_password_v3': ResetPasswordSerializer3,
        'reset_password_confirm_v3': CheckResetPasswordSerializer3,
        'reset_password_complete_v3': ResetPasswordCompleteSerializer3,
    }

    @action(methods=['post'], detail=False, url_path='reset-pass-3', authentication_classes=[])
    @swagger_auto_schema(request_body=ResetPasswordSerializer3)
    def reset_password_v3(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response()

    @action(methods=['post'], detail=False, url_path='reset-pass-confirm-3', authentication_classes=[])
    @swagger_auto_schema(request_body=CheckResetPasswordSerializer3)
    def reset_password_confirm_v3(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response()

    @action(methods=['post'], detail=False, url_path='reset-pass-complete-3', authentication_classes=[])
    @swagger_auto_schema(request_body=ResetPasswordCompleteSerializer3)
    def reset_password_complete_v3(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response()
