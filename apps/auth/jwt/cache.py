from django.conf import settings
from django.core.cache import cache
from rest_framework_jwt.settings import api_settings


class UserActivityStore:
    cache_key_prefix = 'user_auth:'

    def __init__(self, user):
        self.sid = user.sid
        self.uid = user.id

    def logged_out(self):
        cache.set(self.cache_key, self.uid, api_settings.JWT_EXPIRATION_DELTA.total_seconds())

    def is_logout(self):
        return bool(cache.get(self.cache_key))

    @property
    def cache_key(self):
        return self.cache_key_prefix + self.sid
