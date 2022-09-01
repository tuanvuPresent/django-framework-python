import datetime
from urllib.error import HTTPError

from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError
from social_django.utils import load_strategy, load_backend

from apps.auth.jwt.v1.models import RevokedToken
from apps.auth.jwt.v2.serializer import ResetPasswordCompleteSerializer, ResetPasswordSerializer2
from apps.common.jwt_handle import jwt_payload_handler, jwt_encode_handler
from apps.common.custom_exception_handler import CustomAPIException
from apps.common.custom_model_view_set import BaseGenericViewSet


# Create your views here.
class JWTAuthAPIView(BaseGenericViewSet):
    serializer_action_classes = {
        'reset_password_v2': ResetPasswordSerializer2,
        'reset_password_complete_v2': ResetPasswordCompleteSerializer,
    }


    @action(methods=['post'], detail=False, url_path='reset-pass-2', authentication_classes=[])
    @swagger_auto_schema(request_body=ResetPasswordSerializer2)
    def reset_password_v2(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response(data={'token': token})

    @action(methods=['post'], detail=False, url_path='reset-pass-complete-2', authentication_classes=[])
    @swagger_auto_schema(request_body=ResetPasswordCompleteSerializer)
    def reset_password_complete_v2(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response(data='success')
