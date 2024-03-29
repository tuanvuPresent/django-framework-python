from apps.common.models import UuidModel
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class TypeBook(UuidModel):
    name = models.CharField(max_length=64)


class Author(UuidModel):
    name = models.CharField(max_length=64, unique=True)


class Book(UuidModel):
    name = models.CharField(max_length=64, unique=True)
    type_book = models.ForeignKey(
        TypeBook, on_delete=models.CASCADE, related_name='type_book')
    date_of_manufacture = models.DateTimeField()
    author_book = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='author_book', null=True)


@receiver(signal=post_save, sender=Book)
def after_save_book(sender, instance, *args, **kwargs):
    print('after save book then this function run')
