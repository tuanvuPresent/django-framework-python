from rest_framework import routers

from api.paypal import views

router = routers.DefaultRouter()
router.register('paypal', views.PaymentViewSet, basename='paypal')
urlpatterns = router.urls
