from django.conf.urls import url
from django.urls import include
from apps.auth.user_activity.views import UserActivityAPIView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'auth/user-activity', UserActivityAPIView)


urlpatterns = [
    url('auth/', include('apps.auth.authentication.urls')),
    url('auth/', include('apps.auth.jwt.urls')),
    url('', include(router.urls)),
]