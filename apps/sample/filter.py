from django_filters.rest_framework import FilterSet
from django_filters import filters


class BookFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    moth_of_manufacture = filters.CharFilter(field_name='date_of_manufacture__date__month', lookup_expr='exact')
