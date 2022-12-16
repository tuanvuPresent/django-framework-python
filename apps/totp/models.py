from apps.account.models import User
from django.db import models
from apps.common.models import UuidModel


class UserOtpDevice(UuidModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64)
