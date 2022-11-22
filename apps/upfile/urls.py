from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from apps.upfile import views

router = routers.SimpleRouter()
router.register('upload/v1', views.FileUploadView, basename='upload')
router.register('upload/v2', views.FileUploadViewSet, basename='upload')

urlpatterns = [
    url('', include(router.urls)),
]
