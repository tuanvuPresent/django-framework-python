from django.db import models

from apps.common.models import BaseModel


# Create your models here.
class RevokedToken(BaseModel):
    token = models.CharField(max_length=256)
