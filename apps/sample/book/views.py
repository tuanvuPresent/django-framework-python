# Create your views here.
from rest_framework.permissions import IsAuthenticated
from apps.sample.book.filter import BookFilter
from apps.sample.book.models import Book
from apps.sample.book.serializer import BookSerializer
from apps.common.custom_model_view_set import BaseModelViewSet


class BookAPIView(BaseModelViewSet):
    filter_class = BookFilter

    serializer_method_classes = {
        'GET': BookSerializer,
        'POST': BookSerializer,
        'DELETE': BookSerializer,
        'PUT': BookSerializer,
        'PATCH': BookSerializer
    }

    permission_action_classes = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'update': [IsAuthenticated],
        'destroy': [IsAuthenticated]
    }

    def get_queryset(self):
        return Book.objects.all().select_related('type_book')
