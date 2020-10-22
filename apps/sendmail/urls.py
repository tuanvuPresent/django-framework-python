from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.sendmail import views

router = routers.SimpleRouter()
router.register('sendmail', views.SendEmailAPIView, basename='sendmail')
urlpatterns = [
    url('', include(router.urls))
]
