from django.db import models
from enum import Enum
from apps.common.models import UuidModel
from apps.shops.models.category_product import CategoryProduct


class EntityProduct(UuidModel):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.CharField(max_length=256)
    is_visiable = models.BooleanField(default=False)

    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE)


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


class ProductConfig(UuidModel):
    product = models.ForeignKey(EntityProduct, on_delete=models.CASCADE)
    product_config = models.ForeignKey(
        EntityProduct, on_delete=models.CASCADE, related_name='product_config_set', default=None, null=True)
