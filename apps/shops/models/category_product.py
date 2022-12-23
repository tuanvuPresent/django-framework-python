from django.db import models
from apps.common.models import UuidModel


class CategoryProduct(UuidModel):
    name = models.CharField(max_length=63)
    parent = models.ForeignKey('CategoryProduct', on_delete=models.SET_NULL, null=True, default=None)
