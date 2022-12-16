# Create your views here.
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.http import Http404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response

from apps.common.custom_model_view_set import BaseModelViewSet
from apps.common.custom_permission import IsUser, IsUserObjects
from apps.common.serializer import DeleteSerialize
from apps.sample.todos.models import Todo
from apps.sample.todos.serializer import TodoListSerializer, TodoCreateSerializer


@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class TodoAPIView(BaseModelViewSet):
    serializer_method_classes = {
        'GET': TodoListSerializer,
        'POST': TodoCreateSerializer,
        'DELETE': TodoCreateSerializer,
        'PUT': TodoCreateSerializer,
        'PATCH': TodoCreateSerializer
    }
    permission_action_classes = {
        'create': [IsUser],
        'list': [IsUser],
        'retrieve': [IsUserObjects],
        'update': [IsUserObjects],
        'destroy': [IsUserObjects]
    }

    def get_queryset(self):
        return Todo.objects.all().filter(user_id=self.request.user.id)

    @swagger_auto_schema(request_body=DeleteSerialize)
    @action(methods=['DELETE'], detail=False)
    @transaction.atomic()
    def delete(self, request):
        user = request.user
        if type(user) == AnonymousUser:
            raise NotAuthenticated
        pk = request.data.get('pk')
        todo = Todo.objects.filter(id__in=pk, user_id=user)
        if todo.count() != len(pk):
            raise Http404
        todo.delete()
        return Response()
