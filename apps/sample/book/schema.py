import graphene
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation

from apps.sample.book.models import Book, TypeBook, Author
from apps.sample.book.serializer import BookSerializer


class TypeBookObjectType(DjangoObjectType):
    class Meta:
        model = TypeBook
        fields = ["id", "name"]


class AuthorBookObjectType(DjangoObjectType):
    class Meta:
        model = Author
        fields = ["id", "name"]


class BookObjectType(DjangoObjectType):
    type_book = TypeBookObjectType()
    author_book = AuthorBookObjectType()

    class Meta:
        model = Book
        fields = ["id", "name", "type_book", "date_of_manufacture", "author_book"]


class CreateOrUpdateBookMutation(SerializerMutation):
    class Meta:
        serializer_class = BookSerializer


class DeleteBookMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Book.objects.get(pk=kwargs["id"])
        obj.delete()
        return cls(ok=True)


class Query(graphene.ObjectType):
    book_by_name = graphene.Field(BookObjectType, name=graphene.String(required=True))
    all_book = graphene.List(BookObjectType)

    def resolve_book_by_name(root, info, name):
        try:
            return Book.objects.get(name=name)
        except Book.DoesNotExist:
            return None

    def resolve_all_book(root, info):
        return Book.objects.all()


class Mutation(graphene.ObjectType):
    create_or_book = CreateOrUpdateBookMutation.Field()
    delete_book = DeleteBookMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
