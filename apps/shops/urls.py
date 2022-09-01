from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.shops import views

router = routers.SimpleRouter()
router.register('shop/products', views.ProductAPIView, basename='shop')
router.register('shop/order', views.OrderAPIView, basename='shop')
router.register('shop/revenue', views.RevenueAPIView, basename='shop')
urlpatterns = [
    url('', include(router.urls)),
]
