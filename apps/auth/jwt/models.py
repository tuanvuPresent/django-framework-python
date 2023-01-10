from django.db import models
from django.conf import settings

from apps.common.models import UuidModel


class RevokedToken(UuidModel):
    token = models.CharField(max_length=256)


class ResetPasswordReferent(UuidModel):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, models.DO_NOTHING, default=None)
    code = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)


class UserActivity(UuidModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    session_key = models.CharField(max_length=63)
    created_at = models.DateTimeField(auto_now_add=True)
