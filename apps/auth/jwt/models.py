from django.db import models

from apps.account.models import User
from apps.common.models import UuidModel


class RevokedToken(UuidModel):
    token = models.CharField(max_length=256)


class ResetPasswordReferent(UuidModel):
    user_id = models.OneToOneField(User, models.DO_NOTHING, default=None)
    code = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
