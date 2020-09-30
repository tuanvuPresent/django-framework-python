from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.shops import views

router = routers.SimpleRouter()
router.register('products', views.ProductAPIView, basename='products')
router.register('order', views.OrderAPIView, basename='order')
router.register('revenue', views.RevenueAPIView, basename='revenue')
urlpatterns = [
    url('', include(router.urls)),
]
