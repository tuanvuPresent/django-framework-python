from rest_framework import serializers
from django.conf import settings
from apps.shops.models.orders import Order, Revenue
from apps.shops.orders.v1.serializer import ListOrderSerializer


class ListRevenueSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'date', 'total', 'detail']
        model = Revenue
        extra_kwargs = {
            'date': {'format': settings.FORMAT_DATE}
        }

    def get_detail(self, instance):
        queryset = Order.objects.filter(is_pay=True, date_pay=instance.date)
        serializer = ListOrderSerializer(queryset, many=True)
        return serializer.data
