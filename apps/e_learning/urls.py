from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from apps.e_learning.questions.views import QuestionAPIView
from apps.e_learning.config_question.views import ConfigExamAPIView
from apps.e_learning.exams.views import ExamAPIView, DoExamAPIView

router = routers.SimpleRouter()

router.register('e-learning/v1/questions',
                QuestionAPIView, basename='e-learning')
router.register('e-learning/v1/config-question',
                ConfigExamAPIView, basename='e-learning')

router.register('e-learning/v1/exams', ExamAPIView, basename='e-learning')
router.register('e-learning/v1/do_exams',
                DoExamAPIView, basename='e-learning')

urlpatterns = router.urls
