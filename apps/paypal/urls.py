from rest_framework import routers

from apps.paypal import views

router = routers.DefaultRouter()
router.register('paypal', views.PaymentViewSet, basename='paypal')
urlpatterns = router.urls
