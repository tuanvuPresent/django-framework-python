from rest_framework import routers

from apps.auth.jwt.v3 import views

router = routers.DefaultRouter()
router.register('jwt/auth', views.JWTAuthAPIView, basename='jwt_auth')
urlpatterns = router.urls
