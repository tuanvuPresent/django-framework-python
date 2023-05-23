import datetime
from urllib.error import HTTPError

from apps.auth.jwt.signals import user_login, user_logout
from apps.auth.jwt.v1.serializer import JWTLoginSerializer, JWTPasswordChangeSerializer, \
    JWTPasswordResetSerializer, SocialLoginSerializer, JWTRefreshTokenSerializer, JWTAdminLoginSerializer
from apps.common.custom_exception_handler import CustomAPIException
from apps.common.custom_model_view_set import BaseGenericViewSet
from apps.common.jwt_handle import JwtTokenGenerator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError
from social_django.utils import load_strategy, load_backend


class JWTAuthAPIView(BaseGenericViewSet):
    serializer_action_classes = {
        'login': JWTLoginSerializer,
        'admin_login': JWTAdminLoginSerializer,
        'refresh_token': JWTRefreshTokenSerializer,
        'change_password': JWTPasswordChangeSerializer,
        'reset_password': JWTPasswordResetSerializer,
    }

    @action(methods=['post'], detail=False)
    def logout(self, request):
        response = Response(data=None)
        response.delete_cookie(api_settings.JWT_AUTH_COOKIE)
        user_logout.send(sender=request.user.__class__, user=request.user)
        return response

    @swagger_auto_schema(request_body=JWTLoginSerializer)
    @action(methods=['post'], detail=False, authentication_classes=[])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token = serializer.validated_data.get('token')

        data = {
            'token': token,
            'user_id': user.pk,
            'email': user.email
        }
        response = Response(data=data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (
                datetime.datetime.now(datetime.timezone.utc)
                + api_settings.JWT_EXPIRATION_DELTA
            )
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)

        user_login.send(sender=request.user.__class__, user=user)
        return response

    @swagger_auto_schema(request_body=JWTAdminLoginSerializer)
    @action(methods=['post'], detail=False, authentication_classes=[], url_path='admin-login')
    def admin_login(self, request):
        return self.login(request)

    @swagger_auto_schema(request_body=JWTRefreshTokenSerializer)
    @action(methods=['post'], detail=False, url_path='refresh-token')
    def refresh_token(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get('token')
        user = serializer.validated_data.get('user')

        data = {
            'token': token,
            'user_id': user.pk,
            'email': user.email
        }
        response = Response(data=data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (
                datetime.datetime.now(datetime.timezone.utc)
                + api_settings.JWT_EXPIRATION_DELTA
            )
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
        return response

    @swagger_auto_schema(request_body=JWTPasswordChangeSerializer)
    @action(methods=['post'], detail=False, url_path='change-password')
    def change_password(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=None)

    @swagger_auto_schema(request_body=JWTPasswordResetSerializer)
    @action(methods=['post'], detail=False, authentication_classes=[], url_path='reset-pass-1')
    def reset_password(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class AuthSocialView(BaseGenericViewSet):
    serializer_class = SocialLoginSerializer

    @action(methods=['post'], detail=False, authentication_classes=[])
    def login(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)
        try:
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
        except MissingBackend as e:
            raise CustomAPIException(messenger='Please provide a valid provider') from e

        try:
            access_token = None
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)
        except HTTPError as exc:
            raise CustomAPIException('Invalid token') from exc
        except AuthTokenError as exc:
            raise CustomAPIException('Invalid credentials') from exc

        token = JwtTokenGenerator().get_token(user)
        data = {
            "email": user.email,
            "username": user.username,
            "token": token
        }
        response = Response(data=data)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (
                datetime.datetime.now(datetime.timezone.utc)
                + api_settings.JWT_EXPIRATION_DELTA
            )
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
        return response
