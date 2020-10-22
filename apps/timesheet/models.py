from django.db import models

from apps.account.models import User
from apps.common.models import BaseModel


# Create your models here.
class TimeSheet(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timesheet')
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
