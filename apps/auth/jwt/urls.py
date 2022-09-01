from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('v1/', include('apps.auth.jwt.v1.urls')),
    url('v2/', include('apps.auth.jwt.v2.urls')),
    url('v3/', include('apps.auth.jwt.v3.urls')),
]