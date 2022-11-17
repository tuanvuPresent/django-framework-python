from rest_framework import routers

from api.webhook import views

router = routers.SimpleRouter()
router.register('webhook', views.HookViewSet, basename='webhook')
urlpatterns = router.urls
