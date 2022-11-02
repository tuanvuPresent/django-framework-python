from rest_framework import serializers


class AmountSerializer(serializers.Serializer):
    currency_code = serializers.CharField(default='USD')
    value = serializers.CharField()


class PurchaseUnitSerializer(serializers.Serializer):
    reference_id = serializers.CharField()
    amount = AmountSerializer()


class CreateOrderViewRemoteSerializer(serializers.Serializer):
    purchase_units = PurchaseUnitSerializer(many=True)


class CaptureOrderViewSerializer(serializers.Serializer):
    order_id = serializers.CharField()
