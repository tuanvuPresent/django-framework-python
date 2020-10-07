# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.http import Http404
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.account.models import User
from apps.account.serializer import UserSerializer
from apps.account.tasks import send_mail_task
from apps.account.utils import generate_token_register_email, validate_token_verify_email, handle_verify_email
from apps.common.custom_exception_handler import CustomAPIException
from apps.common.custom_model_view_set import BaseModelViewSet
from apps.common.custom_permission import IsAdminUser, IsAdminUserOrIsUserObjects
from apps.common.serializer import DeleteSerialize, NoneSerializer


@method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class RegisterUserAPIView(BaseModelViewSet):
    serializer_action_classes = {
        'register': UserSerializer,
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'update': UserSerializer,
        'partial_update': UserSerializer,
        'delete': DeleteSerialize,
        'register_email': NoneSerializer,
        'verify_email': NoneSerializer,
    }

    permission_action_classes = {
        'create': [AllowAny],
        'list': [IsAdminUser],
        'retrieve': [IsAdminUserOrIsUserObjects],
        'update': [IsAdminUserOrIsUserObjects],
        'destroy': [IsAdminUser],
        'delete': [IsAdminUser]
    }

    def get_queryset(self):
        queryset = User.objects.filter(is_active=True).select_related('profile')
        return queryset

    @swagger_auto_schema(request_body=DeleteSerialize)
    @action(methods=['DELETE'], detail=False)
    @transaction.atomic()
    def delete(self, request):
        pk = request.data['pk']
        user = User.objects.filter(id__in=pk, is_active=True)
        if user.count() != len(pk):
            raise Http404
        user.update(is_active=False)
        return Response()

    @action(methods=['post'], detail=False, authentication_classes=[])
    def register(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    @action(methods=['post'], detail=False, url_path='email/register')
    def register_email(self, request, *args, **kwargs):
        token = generate_token_register_email(request.user)
        body = get_current_site(request).domain + '/api/account/email/verify/?code={}'.format(token)
        if not request.user.email:
            raise CustomAPIException('You do not have email information')
        send_mail_task.delay('VERIFY EMAIL', body, request.user.email)
        return Response(data=None)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('code', openapi.IN_QUERY, type=openapi.TYPE_STRING)])
    @action(methods=['get'], detail=False, authentication_classes=[], url_path='email/verify')
    def verify_email(self, request, *args, **kwargs):
        token = request.query_params.get('code')
        user = validate_token_verify_email(token)
        if not user:
            raise CustomAPIException('verify email fail')
        handle_verify_email(user)
        return Response(data=None)
