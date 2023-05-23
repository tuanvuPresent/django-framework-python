from rest_framework import routers
from apps.sendmail import views

router = routers.SimpleRouter()
router.register('sendmail', views.SendEmailAPIView, basename='sendmail')
urlpatterns = router.urls
