from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('auth/', include('apps.auth.authentication.urls')),
    url('auth/', include('apps.auth.jwt.urls')),
]