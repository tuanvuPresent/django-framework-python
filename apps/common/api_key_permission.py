import hashlib
import secrets
from datetime import datetime

from django.db import models
from django.utils.crypto import get_random_string
from rest_framework.permissions import BasePermission


class APIKeyPermission(models.Model):
    name = models.CharField(max_length=63, unique=True)
    scope = models.CharField(max_length=63)
    prefix = models.CharField(max_length=16, unique=True, editable=False)
    key = models.CharField(max_length=255, unique=True, editable=False)
    revoked = models.BooleanField(default=False)
    expiry_date = models.DateTimeField(blank=True, null=True)

    def gen_key(self):
        prefix = secrets.token_hex(8)
        secret_key = secrets.token_hex(32)
        key = f'{prefix}.{secret_key}'.encode()
        hashed_key = hashlib.sha256(key).hexdigest()
        return prefix, hashed_key

    def hash_key(self, key):
        hashed_key = hashlib.sha256(key).hexdigest()
        return hashed_key

    def is_valid(self, key):
        hashed_key = self.hash_key(key.encode())
        now = datetime.now()

        if self.key == hashed_key and not self.revoked and (not self.expiry_date or self.expiry_date > now):
            return True
        return False

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.prefix, self.key = self.gen_key()
        super().save()


class CustomHasAPIKey(BasePermission):
    def has_permission(self, request, view):
        api_key = 'aOvzLPsk.UOIhh30FJiZo37fqKWv1LbMxIKT8Kyem'
        if api_key:
            try:
                api_key_obj = APIKeyPermission.objects.get(prefix=api_key.split('.')[0])
                return api_key_obj.is_valid(api_key) and api_key_obj.scope == view.scope
            except APIKeyPermission.DoesNotExist:
                return False

        return False
