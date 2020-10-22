from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.authentication_jwt import views

router = routers.DefaultRouter()
router.register('jwt/auth', views.JWTAuthAPIView, basename='jwt_auth')
router.register('jwt/auth/social', views.AuthSocialView, basename='jwt_auth')
urlpatterns = [
    url('', include(router.urls)),
]
