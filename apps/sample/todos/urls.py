from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.sample.todos import views

router = routers.SimpleRouter()
router.register('todos', views.TodoAPIView, basename='todo')

urlpatterns = [
    url('', include(router.urls)),
]
