from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.auth.authentication.custom_authentication import is_expired
from apps.auth.authentication.serializer import LoginSerializer, PasswordChangeSerializer, PasswordResetSerializer
from apps.common.custom_model_view_set import BaseGenericViewSet


# Create your views here.
class AuthAPIView(BaseGenericViewSet):
    serializer_action_classes = {
        'login': LoginSerializer,
        'change_password': PasswordChangeSerializer,
        'reset_password': PasswordResetSerializer,
    }

    @action(methods=['get'], detail=False)
    def logout(self, request):
        user = request.user
        if user.is_authenticated:
            Token.objects.get(user=user).delete()
        return Response()

    @swagger_auto_schema(request_body=LoginSerializer)
    @action(methods=['post'], detail=False, authentication_classes=[])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        if is_expired(token):
            token.delete()
            token = Token.objects.create(user=user)

        data = {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }
        return Response(data=data)

    @swagger_auto_schema(request_body=PasswordChangeSerializer)
    @action(methods=['post'], detail=False)
    def change_password(self, request):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=PasswordResetSerializer)
    @action(methods=['post'], detail=False, authentication_classes=[])
    def reset_password(self, request):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)
