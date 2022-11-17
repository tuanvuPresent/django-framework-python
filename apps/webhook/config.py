from django.conf import settings
from rest_framework.settings import APISettings

WEBHOOK_SETTING = getattr(settings, 'HOOK_EVENTS', None)
DEFAULTS = {

}
webhook_settings = APISettings(WEBHOOK_SETTING, DEFAULTS)
