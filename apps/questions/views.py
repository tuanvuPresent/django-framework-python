# Create your views here.
from django.db import transaction
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.common.custom_model_view_set import BaseModelViewSet
from apps.common.custom_permission import IsAdminUser
from apps.common.serializer import DeleteSerialize
from apps.exams.models import Exams, Configuration
from apps.questions.models import Question, Answer
from apps.questions.serializer import ListQuestionSerializer, CreateQuestionSerializer
from apps.questions.utils import update_exams, update_exam_config


@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class QuestionAPIView(BaseModelViewSet):
    serializer_method_classes = {
        'GET': ListQuestionSerializer,
        'POST': CreateQuestionSerializer,
        'DELETE': CreateQuestionSerializer,
        'PUT': CreateQuestionSerializer,
        'PATCH': CreateQuestionSerializer
    }
    permission_action_classes = {
        'create': [IsAdminUser],
        'list': [IsAdminUser],
        'retrieve': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser]
    }

    def get_queryset(self):
        return Question.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                'answers',
                queryset=Answer.objects.filter(is_active=True),
            )
        ).select_related('category_id')

    @transaction.atomic()
    @swagger_auto_schema(request_body=DeleteSerialize)
    @action(methods=['DELETE'], detail=False)
    def delete(self, request):
        pk = request.data['pk']
        questions = Question.objects.filter(is_active=True, id__in=pk)
        if questions.count() != len(pk):
            raise NotFound()
        questions.update(is_active=False)

        exams = set(Exams.objects.filter(is_active=True, question_id__in=pk))
        update_exams(questions, exams)
        update_exam_config(questions, exams)

        return Response()