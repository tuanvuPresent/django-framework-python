from rest_framework.viewsets import ModelViewSet
from apps.shops.models import EntityProduct
from apps.shops.product.v1.serializers import EntityProductSerializerList


class EntityProductApiView(ModelViewSet):
    queryset = EntityProduct.objects.all()
    serializer_class = EntityProductSerializerList
