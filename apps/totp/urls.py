from rest_framework import routers

from apps.totp import views

router = routers.DefaultRouter()
router.register('totp', views.AuthOtpViewSet, basename='totp')
urlpatterns = router.urls
