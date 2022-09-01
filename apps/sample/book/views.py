# Create your views here.
from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework.permissions import IsAuthenticated

from apps.sample.book.models import Book
from apps.sample.book.serializer import BookSerializer
from apps.common.custom_model_view_set import BaseModelViewSet


class BookFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    moth_of_manufacture = filters.CharFilter(field_name='date_of_manufacture__date__month', lookup_expr='exact')


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
