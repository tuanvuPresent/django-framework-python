from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('', include('apps.account.urls')),
    url('', include('apps.auth.urls')),
    url('', include('apps.e_learning.urls')),
    url('', include('apps.export_file.urls')),
    url('', include('apps.fcm_notify.urls')),
    url('', include('apps.import_file.urls')),
    url('', include('apps.my_phone_verify.urls')),
    url('', include('apps.paypal.urls')),
    url('', include('apps.sample.urls')),
    url('', include('apps.sample_els.urls')),
    url('', include('apps.sendmail.urls')),
    url('', include('apps.shops.urls')),
    url('', include('apps.totp.urls')),
    url('', include('apps.upfile.urls')),
    url('', include('apps.webhook.urls')),
]
