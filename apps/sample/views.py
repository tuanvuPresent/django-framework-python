from rest_framework.permissions import IsAuthenticated
from apps.sample.filter import BookFilter
from apps.sample.models import Book
from apps.sample.serializer import BookSerializer
from apps.common.custom_model_view_set import BaseModelViewSet


class BookAPIView(BaseModelViewSet):
    filterset_class = BookFilter
    throttle_scope = 'sample_rates'
    queryset = Book.objects.all().select_related('type_book')

    serializer_action_classes = {
        'create': BookSerializer,
        'list': BookSerializer,
        'retrieve': BookSerializer,
        'update': BookSerializer,
        'partial_update': BookSerializer,
    }

    permission_action_classes = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'update': [IsAuthenticated],
        'destroy': [IsAuthenticated]
    }
