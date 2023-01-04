from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.auth.jwt.v1 import views

router = routers.DefaultRouter()
router.register('jwt/auth', views.JWTAuthAPIView, basename='jwt_auth')
router.register('jwt/auth/social', views.AuthSocialView, basename='jwt_auth')
urlpatterns = router.urls
