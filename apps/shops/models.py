from django.db import models

from apps.account.models import User
from apps.common.models import BaseModel


# Create your models here.
class TypeProduct(BaseModel):
    name = models.CharField(max_length=64)


class Product(BaseModel):
    type_id = models.ForeignKey(TypeProduct, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=64, unique=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    image = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=256)
    date = models.DateField(auto_now_add=True)
    number_of_view = models.IntegerField(default=0)
    sale_off = models.IntegerField(default=0)


class Promotion(BaseModel):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promotion_product')
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    discount = models.CharField(max_length=64)


class Order(BaseModel):
    user_order = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    address = models.CharField(max_length=64)
    phone = models.TextField(max_length=16)
    created_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.CharField(max_length=64)
    is_pay = models.BooleanField(default=False)
    date_pay = models.DateField(default=None, null=True)

    class Meta:
        ordering = ['-created_date']


class OrderDetail(BaseModel):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_detail')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    product_quantity = models.IntegerField()
    product_price = models.IntegerField(default=0)
    amount = models.CharField(max_length=64, null=True)


class Revenue(BaseModel):
    date = models.DateField(auto_now_add=True)
    total = models.CharField(max_length=64, default=None, null=True)
