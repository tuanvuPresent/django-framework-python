from rest_framework import routers

from apps.my_phone_verify import views

router = routers.SimpleRouter()
router.register('phone', views.VerificationPhoneView, basename='phone')

urlpatterns = router.urls
