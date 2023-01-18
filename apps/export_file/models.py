from django.db import models
from enum import Enum
from apps.common.models import UuidModel

class DownloadFileLog(UuidModel):
    class StatusType(Enum):
        IN_PROCESS = 0
        SUCCESS = 1
        FAIL = 2

    path = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    status = models.IntegerField(choices=[(tag, tag.value) for tag in StatusType], default=StatusType.IN_PROCESS.value)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)