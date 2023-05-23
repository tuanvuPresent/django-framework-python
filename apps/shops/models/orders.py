from django.db import models
from apps.account.models import User
from apps.common.models import UuidModel
from apps.shops.models.product import EntityProduct


class Promotion(UuidModel):
    product = models.ForeignKey(EntityProduct, on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    discount = models.CharField(max_length=64)


class Order(UuidModel):
    user_order = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone = models.TextField(max_length=16)
    created_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.CharField(max_length=64)
    is_pay = models.BooleanField(default=False)
    date_pay = models.DateField(default=None, null=True)

    class Meta:
        ordering = ['-created_date']


class OrderDetail(UuidModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(EntityProduct, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
    product_price = models.IntegerField(default=0)
    amount = models.CharField(max_length=64, null=True)


class Revenue(UuidModel):
    date = models.DateField(auto_now_add=True)
    total = models.CharField(max_length=64, default=None, null=True)
