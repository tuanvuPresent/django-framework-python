from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.sample.book import views

router = routers.SimpleRouter()
router.register('books', views.BookAPIView, basename='books')

urlpatterns = [
    url('', include(router.urls)),
]
