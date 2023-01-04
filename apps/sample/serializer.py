from rest_framework import serializers

from apps.sample.models import Book, TypeBook


class TypeBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeBook
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    type_book = TypeBookSerializer()

    class Meta:
        model = Book
        fields = ['id', 'name', 'type_book', 'date_of_manufacture']

    def create(self, validated_data):
        type_book = validated_data.pop('type_book')
        name_type = type_book.get('name')

        type_book, is_create = TypeBook.objects.get_or_create(name=name_type)
        book = Book.objects.create(type_book=type_book, **validated_data)

        return book

    def update(self, instance, validated_data):
        type_book = validated_data.pop('type_book')
        name_type = type_book.get('name')
        instance = super().update(instance, validated_data)

        type_book, is_create = TypeBook.objects.get_or_create(name=name_type)
        instance.type_book = type_book
        instance.save()

        return instance
