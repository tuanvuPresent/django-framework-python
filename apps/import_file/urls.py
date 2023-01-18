from apps.import_file.views import ImportAPIView
from rest_framework import routers

router = routers.SimpleRouter()
router.register('import/v1', ImportAPIView, basename='import')
urlpatterns = router.urls
