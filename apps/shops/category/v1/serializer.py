from rest_framework import serializers

from apps.shops.models.category_product import CategoryProduct


class CategoryProductSerialize(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
        model = CategoryProduct
