from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.shops.category.v1.views import CategoryProductApiView
from apps.shops.product.v1.views import EntityProductApiView
from apps.shops.orders.v1.views import OrderAPIView
from apps.shops.statistics.v1.views import RevenueAPIView

router = routers.SimpleRouter()
router.register('shop/v1/category', CategoryProductApiView, basename='shop')
router.register('shop/v1/products', EntityProductApiView, basename='shop')
router.register('shop/v1/order', OrderAPIView, basename='shop')
router.register('shop/v1/statistics', RevenueAPIView, basename='shop')


urlpatterns = [
    url('', include(router.urls)),
]
