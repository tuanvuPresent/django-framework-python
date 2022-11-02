from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.paypal.serializer import CaptureOrderViewSerializer, CreateOrderViewRemoteSerializer
from api.paypal.paypal_service import PayPalService


class PaymentViewSet(GenericViewSet):
    pagination_class = None

    @action(methods=['POST'], detail=False, url_path='order')
    @swagger_auto_schema(request_body=CreateOrderViewRemoteSerializer)
    def create_order(self, request):
        purchase_units = request.data.get('purchase_units')

        response = PayPalService().create_order(purchase_units)
        return Response(response.json()['links'])

    @action(methods=['POST'], detail=False, url_path='capture', authentication_classes=[])
    @swagger_auto_schema(request_body=CaptureOrderViewSerializer)
    def capture(self, request):
        order_id = request.data.get('order_id')

        response = PayPalService().capture_order(order_id)
        return Response(response.json())
