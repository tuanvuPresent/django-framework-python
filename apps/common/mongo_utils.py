from collections import OrderedDict
from django_filters import FilterSet
from django_filters.constants import EMPTY_VALUES
from mongoengine import DynamicDocument, DoesNotExist, ValidationError, Q
from rest_framework.exceptions import NotFound

from apps.common.custom_model_view_set import BaseModelViewSet


class DocumentRepositoryBase(object):
    class Meta:
        model = DynamicDocument

    @classmethod
    def all(cls):
        return cls.Meta.model.objects()

    @classmethod
    def count(cls, queryset):
        return queryset.count()

    @classmethod
    def get_object_or_404(cls, queryset, filter_kwargs):
        try:
            return queryset.get(**filter_kwargs)
        except (ValueError, TypeError, DoesNotExist, ValidationError) as e:
            raise NotFound() from e

    @classmethod
    def create(cls, data):
        return cls.Meta.model(**data).save()

    @classmethod
    def update(cls, instance, data):
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @classmethod
    def delete(cls, instance):
        instance.delete()
        return instance

    @classmethod
    def filter_queryset(cls, queryset, filter_kwargs):
        return queryset.filter(filter_kwargs)

    @classmethod
    def paginate_queryset(cls, queryset, paginate):
        return list(queryset[paginate.offset:paginate.offset + paginate.limit])

    @classmethod
    def ordering_queryset(cls, queryset, ordering):
        return queryset.order_by(*ordering) if ordering else queryset

    @classmethod
    def save(cls, instance):
        instance.save()
        return instance


class MongoFilterSet(FilterSet):

    def get_form_class(self):
        fields = OrderedDict(
            [(name, filter_.field) for name, filter_ in self.base_filters.items()]
        )
        return type(str(f"{self.__class__.__name__}Form"), (self._meta.form,), fields)

    @classmethod
    def get_filter_kwargs(cls, query_params):
        filter_kwargs = {}
        for name, field in cls.base_filters.items():
            value = query_params.get(name)
            if value not in EMPTY_VALUES and not field.exclude:
                lookup = f"{field.field_name}__{field.lookup_expr}"
                filter_kwargs[lookup] = value
        return Q(**filter_kwargs)


class BaseMongoModelViewSet(BaseModelViewSet):
    lookup_field = 'id'
    repository_class = DocumentRepositoryBase

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = self.repository_class.get_object_or_404(queryset, filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_filter_kwargs(self):
        self.queryset.model = self.repository_class.Meta.model
        return super().get_filter_kwargs()
