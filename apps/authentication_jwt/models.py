from django.db import models

from apps.account.models import User
from apps.common.models import BaseModel


# Create your models here.
class RevokedToken(BaseModel):
    token = models.CharField(max_length=256)


class ResetPasswordReferent(models.Model):
    user_id = models.OneToOneField(User, models.DO_NOTHING, default=None)
    code = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
