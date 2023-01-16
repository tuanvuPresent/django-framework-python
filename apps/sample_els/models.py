from django.db import models
from apps.common.uuid_gen import uuid
from apps.common.models import UuidModel


class Sample(UuidModel):
    name = models.CharField(max_length=64, unique=True)
    date_of_manufacture = models.DateTimeField()
