from rest_framework import routers

from apps.sample_els.views import SampleDocumentApiView

router = routers.DefaultRouter()
router.register('sample-esl', SampleDocumentApiView, basename='sample-esl')

urlpatterns = router.urls
