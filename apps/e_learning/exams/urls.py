from rest_framework import routers

from apps.e_learning.exams import views

router = routers.SimpleRouter()
router.register('exams', views.ExamAPIView, basename='exams')
router.register('exams_config', views.ConfigExamAPIView, basename='exams_config')
router.register('do_exams', views.DoExamAPIView, basename='do_exams')
urlpatterns = router.urls
