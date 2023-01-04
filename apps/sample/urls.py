from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.sample import views

router = routers.SimpleRouter()
router.register('sample/v1/book', views.BookAPIView, basename='sample')

urlpatterns = router.urls
