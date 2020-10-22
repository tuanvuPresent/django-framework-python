from rest_framework import routers

from apps.fcm_notify import views

router = routers.DefaultRouter()
router.register('fcm', views.FcmNotifyAPIView, basename='fcm')
urlpatterns = router.urls
