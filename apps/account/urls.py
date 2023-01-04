from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.account import views

router = routers.SimpleRouter()
router.register('account', views.RegisterUserAPIView, basename='account')
urlpatterns = router.urls
