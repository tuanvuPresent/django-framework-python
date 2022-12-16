from datetime import date

from django.db import transaction
from django.db.models import Prefetch
from django.http import Http404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from apps.common.custom_model_view_set import BaseModelViewSet, BaseGenericViewSet
from apps.common.custom_permission import IsAdminUser, IsUser, IsAdminUserOrIsUserObjects
from apps.common.serializer import DeleteSerialize
from apps.shops.handle_shop import update_quantity_product
from apps.shops.serializer import *


# Create your views here.
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class ProductAPIView(BaseModelViewSet):
    throttle_scope = 'shops.request'

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['number_of_view']
    ordering = ['-number_of_view']
    search_fields = ['name']

    serializer_method_classes = {
        'GET': ListProductSerializer,
        'POST': CreateProductSerializer,
        'DELETE': DeleteSerialize,
        'PUT': CreateProductSerializer,
        'PATCH': CreateProductSerializer
    }

    permission_action_classes = {
        'create': [IsAdminUser],
        'list': [IsAdminUser],
        'retrieve': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser]
    }

    def get_queryset(self):
        queryset = Product.objects.all().select_related('type_id')
        return queryset

    @transaction.atomic()
    @swagger_auto_schema(request_body=DeleteSerialize)
    @action(methods=['delete'], detail=False)
    def delete(self, request):
        pk = request.data.get('pk')
        product = Product.objects.filter(id__in=pk)
        if product.count() != len(pk):
            raise Http404
        product.delete()
        return Response()


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
        if self.request.method == 'GET':
            queryset = Order.objects.all().prefetch_related(
                Prefetch(
                    'order_detail',
                    queryset=OrderDetail.objects.all()
                )
            )
        else:
            queryset = Order.objects.filter(is_pay=False).prefetch_related(
                Prefetch(
                    'order_detail',
                    queryset=OrderDetail.objects.all()
                )
            )
        return queryset

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


class RevenueAPIView(ListModelMixin,
                     RetrieveModelMixin,
                     BaseGenericViewSet):
    throttle_scope = 'shops.request'

    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['date']
    ordering = ['date']
    search_fields = ['date']

    serializer_method_classes = {
        'GET': ListRevenueSerializer,
    }

    permission_action_classes = {
        'list': [IsAdminUser],
        'retrieve': [IsAdminUser],
    }

    def get_queryset(self):
        queryset = Revenue.objects.all()
        return queryset
