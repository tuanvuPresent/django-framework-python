from rest_framework.exceptions import ValidationError

from apps.shops.models.orders import OrderDetail


def update_quantity_product(order):
    queryset = OrderDetail.objects.filter(order_id=order)
    for order_detail in queryset:
        product = order_detail.product_id
        product.quantity -= order_detail.product_quantity
        if product.quantity < 0:
            raise ValidationError('Not enough quantity to order')
        product.save()
