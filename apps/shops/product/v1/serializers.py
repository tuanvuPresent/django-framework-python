from rest_framework import serializers
from apps.shops.models import EntityProduct


class EntityProductSerializerList(serializers.ModelSerializer):
    class Meta:
        model = EntityProduct
        fields = ('id', 'name')
