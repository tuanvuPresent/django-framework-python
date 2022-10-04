from django.contrib import admin

# Register your models here.
from apps.sample.book.models import Author, Book, TypeBook

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(TypeBook)
