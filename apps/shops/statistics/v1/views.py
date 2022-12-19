from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from apps.common.custom_model_view_set import BaseGenericViewSet
from apps.common.custom_permission import IsAdminUser
from apps.shops.models.orders import Revenue
from apps.shops.statistics.v1.serializer import ListRevenueSerializer

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
