from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.questions import views

router = routers.SimpleRouter()
router.register('questions', views.QuestionAPIView, basename='questions')
urlpatterns = [
    url('', include(router.urls))
]
