from django.db import models
from enum import Enum
from apps.common.models import UuidModel


class EntityProduct(UuidModel):
    name = models.CharField(max_length=255)
    is_visiable = models.BooleanField(default=False)


class AttributeProduct(UuidModel):
    class ValueType(Enum):
        STR = 0
        INT = 1
        BOOL = 2
    name = models.CharField(max_length=31)
    type_value = models.SmallIntegerField(choices=[(
        item.value, item.value) for item in ValueType], default=ValueType.STR.value)


class ValueEntity(UuidModel):
    entity = models.ForeignKey(EntityProduct, on_delete=models.CASCADE)
    attribute = models.ForeignKey(AttributeProduct, on_delete=models.CASCADE)
    int_value = models.IntegerField()
    str_value = models.CharField(max_length=255)


class TypeProduct(UuidModel):
    name = models.CharField(max_length=64)


class Product(UuidModel):
    type_id = models.ForeignKey(
        TypeProduct, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=64, unique=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    image = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    number_of_view = models.IntegerField(default=0)
    sale_off = models.IntegerField(default=0)
