from django.db import models

from apps.account.models import User
from apps.common.models import UuidModel


# Create your models here.
class Todo(UuidModel):
    user_id = models.ForeignKey(User, models.CASCADE, related_name='todos')
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    title = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512)
