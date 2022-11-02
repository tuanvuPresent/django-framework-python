from django.conf import settings
from rest_framework.settings import APISettings

PAYPAL_SETTING = getattr(settings, 'PAYPAL_SETTING', None)
DEFAULTS = {
    'PAYPAL_ENV': 'develop',
    'CLIENT_ID': '',
    'CLIENT_SECRET': '',
}
paypal_settings = APISettings(PAYPAL_SETTING, DEFAULTS)
