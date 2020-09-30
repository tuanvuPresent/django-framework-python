from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include
from rest_framework import routers

from Example import settings
from apps.upfile import views

router = routers.SimpleRouter()
router.register('upload', views.FileUploadView, basename='upload')

urlpatterns = [
    url('', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
