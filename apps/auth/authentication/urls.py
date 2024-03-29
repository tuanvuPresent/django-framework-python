from rest_framework import routers

from apps.auth.authentication import views

router = routers.DefaultRouter()
router.register('auth', views.AuthAPIView, basename='auth')
urlpatterns = router.urls
