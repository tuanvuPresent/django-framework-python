from rest_framework.viewsets import ModelViewSet
from apps.shops.category.v1.serializer import CategoryProductSerialize
from apps.shops.models.category_product import CategoryProduct


class CategoryProductApiView(ModelViewSet):
    serializer_class = CategoryProductSerialize
    queryset = CategoryProduct.objects.all()
