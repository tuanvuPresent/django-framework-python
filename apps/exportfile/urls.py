from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from apps.exportfile import views

router = routers.SimpleRouter()
router.register('export', views.ExportAPIView, basename='export')
router.register('import', views.ImportAPIView, basename='import')
router.register('export/pdf', views.ExportPdfAPIView, basename='export')
urlpatterns = [
    url('', include(router.urls)),
]
