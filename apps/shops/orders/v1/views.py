from datetime import date

from apps.common.custom_model_view_set import BaseModelViewSet
from apps.common.custom_permission import IsAdminUser, IsUser
from apps.common.serializer import DeleteSerialize
from apps.shops.handle_shop import update_quantity_product
from apps.shops.orders.v1.serializer import *
from django.db import transaction
from django.db.models import Prefetch
from django.http import Http404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response


@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class OrderAPIView(BaseModelViewSet):
    throttle_scope = 'shops.request'

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['user_order']
    ordering = ['-user_order']
    search_fields = ['user_order']

    serializer_method_classes = {
        'POST': CreateOrderSerializer,
        'GET': ListOrderSerializer,
        'PUT': CreateOrderSerializer,
        'DELETE': DeleteSerialize,
        'PATCH': CreateOrderSerializer,
    }

    permission_action_classes = {
        'create': [IsUser],
        'list': [IsUser],
        'retrieve': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
        'payment_confirmation': [IsAdminUser]
    }

    def get_queryset(self):
        return (
            Order.objects.all().prefetch_related(
                Prefetch('order_detail', queryset=OrderDetail.objects.all())
            )
            if self.request.method == 'GET'
            else Order.objects.filter(is_pay=False).prefetch_related(
                Prefetch('order_detail', queryset=OrderDetail.objects.all())
            )
        )

    @transaction.atomic()
    @swagger_auto_schema(request_body=DeleteSerialize)
    @action(methods=['DELETE'], detail=False)
    def delete(self, request):
        pk = request.data.get('pk')
        order = Order.objects.filter(id__in=pk)
        if order.count() != len(pk):
            raise Http404
        order.delete()
        return Response()

    @swagger_auto_schema(request_body=PaymentConfirmSerializer)
    @action(methods=['POST'], detail=False)
    @transaction.atomic()
    def payment_confirmation(self, request):
        pk = request.data.get('order_id')
        order = Order.objects.filter(is_pay=False, id__in=pk)

        if len(pk) != order.count():
            raise serializers.ValidationError('Those orders were payment')

        for order_item in order:
            order_item.is_pay = True
            order_item.date_pay = date.today()
            order_item.save()
            update_quantity_product(order_item)

        return Response()
