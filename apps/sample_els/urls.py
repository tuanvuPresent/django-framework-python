from rest_framework import routers

from apps.sample_els.views import SampleDocumentApiView

router = routers.DefaultRouter()
router.register('sample-els', SampleDocumentApiView, basename='sample-els')

urlpatterns = router.urls
