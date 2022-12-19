from django.db import models
from apps.common.models import UuidModel


class CategoryProduct(UuidModel):
    name = models.CharField(max_length=63)
