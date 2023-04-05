from django.db import transaction
from django.db.models import Prefetch
from django.http import Http404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from apps.common.custom_model_view_set import BaseModelViewSet, BaseGenericViewSet
from apps.common.custom_permission import IsAdminUser, IsUser, IsAdminUserOrIsUserObjects
from apps.common.serializer import DeleteSerialize
from apps.e_learning.exams.serializer import *
from apps.e_learning.exams.utils import get_score


@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class ExamAPIView(BaseModelViewSet):
    throttle_scope = 'exams.request'

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']

    serializer_method_classes = {
        'GET': ListExamSerializer,
        'POST': CreateExamSerializer,
        'DELETE': DeleteSerialize,
        'PUT': CreateExamSerializer,
        'PATCH': CreateExamSerializer
    }

    permission_action_classes = {
        'create': [IsAdminUser],
        'list': [IsAdminUser],
        'retrieve': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser]
    }

    def get_queryset(self):
        return (
            Exams.objects.all()
            .select_related('exam_config_id')
            .select_related('topic_id')
        )

    @transaction.atomic()
    @swagger_auto_schema(request_body=DeleteSerialize)
    @action(methods=['delete'], detail=False)
    def delete(self, request):
        pk = request.data.get('pk')
        exams = Exams.objects.filter(id__in=pk)
        if exams.count() != len(pk):
            raise Http404
        exams.delete()
        return Response()


class DoExamAPIView(RetrieveModelMixin,
                    BaseGenericViewSet
                    ):
    throttle_scope = 'do_exams'

    permission_action_classes = {
        'submit': [IsUser],
        'history': [IsAdminUserOrIsUserObjects],
        'retrieve': [IsUser]
    }
    serializer_action_classes = {
        'retrieve': ListDoExamSerializer,
        'history': HistoryExamSerialize,
        'submit': DoExamSerializer,
    }

    def get_queryset(self):
        return Exams.objects.all().select_related('topic_id').select_related('exam_config_id')

    @transaction.atomic()
    @swagger_auto_schema(request_body=DoExamSerializer)
    @action(methods=['post'], detail=False)
    def submit(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        exam_id = data.get('exam_id')
        your_answers = data.get('answers')
        exam_id = get_object_or_404(Exams, pk=exam_id)
        question = dict(exam_id.question_id.values_list('pk', 'key'))
        correct_answer = {str(id): key for id, key in question.items()}
        score, detail = get_score(correct_answer, your_answers)

        history_exam = HistoryExam.objects.create(
            user_id=request.user,
            score=score,
            exam_id=exam_id,
            number_of_question_correct=score
        )
        data = {
            'result': history_exam,
            'detail': detail
        }
        serializer = DetailResultDoExamSerializer(data)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def history(self, request):
        data = HistoryExam.objects.filter(user_id=request.user)
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)
