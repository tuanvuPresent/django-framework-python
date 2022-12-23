from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.conf import settings
from apps.shops.models.orders import OrderDetail, Order


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['product', 'product_quantity', 'product_price', 'amount']
        model = OrderDetail
        read_only_fields = ['product_price', 'amount']

    def validate(self, data):
        data = super(OrderDetailSerializer, self).validate(data)
        product = data.get('product')
        data['product_price'] = product.price
        data['amount'] = product.price * data.get('product_quantity')
        return data


class ListOrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True)

    class Meta:
        fields = ['id', 'user_order', 'address', 'phone',
                  'created_date', 'total_amount', 'is_pay', 'order_detail']
        model = Order
        extra_kwargs = {
            'created_date': {'format': settings.FORMAT_DATETIME}
        }


class CreateOrderSerializer(serializers.ModelSerializer):
    order_detail = OrderDetailSerializer(many=True)

    class Meta:
        fields = ['user_order', 'address', 'phone',
                  'created_date', 'total_amount', 'order_detail']
        model = Order
        read_only_fields = ['total_amount']
        extra_kwargs = {
            'created_date': {'format': settings.FORMAT_DATETIME}
        }

    def to_internal_value(self, data):
        request = self.context.get('request')
        data['user_order'] = request.user.pk
        return super(CreateOrderSerializer, self).to_internal_value(data)

    def validate(self, data):
        order_detail_data = data.get('order_detail')
        for order_detail_item in order_detail_data:
            product = order_detail_item.get('product')
            product_quantity = order_detail_item.get('product_quantity')
            if product_quantity > product.quantity:
                raise ValidationError(
                    'product_quantity of product {} must <= {}'.format(
                        product.pk, product.quantity)
                )

        return data

    def validate_order_detail(self, data):
        fields = ['product']
        data_copy = []
        for e in data:
            temp = {}
            for k, v in e.items():
                if k in fields:
                    temp[k] = v
            data_copy.append(temp)

        list_order = []
        for item in data_copy:
            if item not in list_order:
                list_order.append(item)

        if len(data) != len(list_order):
            raise ValidationError('order is not overlap')
        return data

    def create(self, validated_data):
        order_detail_data = validated_data.pop('order_detail')
        order = Order.objects.create(**validated_data)

        order_detail_list = [OrderDetail(
            order_id=order, **order_detail) for order_detail in order_detail_data]
        OrderDetail.objects.bulk_create(order_detail_list)

        total_amount = 0
        for order_detail in order_detail_data:
            total_amount += order_detail['amount']
        order.total_amount = total_amount

        order.save()
        return order

    def update(self, instance, validated_data):
        order_detail_data = validated_data.pop('order_detail')
        instance = super(CreateOrderSerializer, self).update(
            instance, validated_data)

        OrderDetail.objects.filter(order_id=instance).delete()
        order_detail_list = [OrderDetail(order_id=instance, **order_detail_item) for order_detail_item in
                             order_detail_data]
        OrderDetail.objects.bulk_create(order_detail_list)

        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user_order', 'address', 'phone',
                  'created_date', 'total_amount']


class PaymentConfirmSerializer(serializers.Serializer):
    order_id = serializers.ListField(child=serializers.IntegerField())
