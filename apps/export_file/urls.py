from apps.export_file.v1.views import ExportAPIView, ExportPdfV1APIView, ExportPdfV2APIView, ExportPdfV3APIView
from apps.export_file.v2.views import ExportV2APIView
from apps.export_file.v3.views import SampleExportApiView
from rest_framework import routers

router = routers.SimpleRouter()
router.register('export/v1', ExportAPIView, basename='export')
router.register('export/v2', ExportV2APIView, basename='export')
router.register('export/v3', SampleExportApiView, basename='export')
router.register('export/v1/pdf', ExportPdfV1APIView, basename='export')
router.register('export/v2/pdf', ExportPdfV2APIView, basename='export')
router.register('export/v3/pdf', ExportPdfV3APIView, basename='export')
urlpatterns = router.urls
