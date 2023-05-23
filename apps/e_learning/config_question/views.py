from apps.common.custom_model_view_set import BaseModelViewSet
from apps.common.custom_permission import IsAdminUser
from apps.common.serializer import DeleteSerialize
from django.db import transaction
from django.db.models import Prefetch
from django.http import Http404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from apps.e_learning.models.exam import Exams, ExamConfiguration, Configuration
from apps.e_learning.config_question.serializer import CreateExamConfigSerializer, ListExamConfigSerializer


@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class ConfigExamAPIView(BaseModelViewSet):
    throttle_scope = 'config_exams.request'

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']

    serializer_method_classes = {
        'GET': ListExamConfigSerializer,
        'POST': CreateExamConfigSerializer,
        'DELETE': DeleteSerialize,
        'PUT': CreateExamConfigSerializer,
        'PATCH': CreateExamConfigSerializer
    }

    permission_action_classes = {
        'create': [IsAdminUser],
        'list': [IsAdminUser],
        'retrieve': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser]
    }

    def get_queryset(self):
        return ExamConfiguration.objects.all().prefetch_related(
            Prefetch(
                'config',
                queryset=Configuration.objects.all(),
            )
        )

    @transaction.atomic()
    @swagger_auto_schema(request_body=DeleteSerialize)
    @action(methods=['delete'], detail=False)
    def delete(self, request):
        pk = request.data.get('pk')
        exam_config = ExamConfiguration.objects.filter(id__in=pk)
        if exam_config.count() != len(pk):
            raise Http404
        exam_config.delete()
        Exams.objects.filter(exam_config_id__in=pk).delete()
        return Response()
