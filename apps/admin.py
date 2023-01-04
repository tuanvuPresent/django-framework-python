from django.contrib import admin
from django.contrib.auth import get_user_model
from apps.sample.book.models import Author, Book, TypeBook

User = get_user_model()

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(TypeBook)
admin.site.register(User)