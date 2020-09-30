# Create your views here.

from django.db import transaction
from django.http import Http404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.account.models import User
from apps.account.serializer import UserSerializer
from apps.common.custom_model_view_set import BaseModelViewSet
from apps.common.custom_permission import IsAdminUser, IsAdminUserOrIsUserObjects
from apps.common.serializer import DeleteSerialize


@method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class RegisterUserAPIView(BaseModelViewSet):
    serializer_class = UserSerializer

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
