from django.contrib.auth.models import User
from django.db import models


class UserOtpDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64)
