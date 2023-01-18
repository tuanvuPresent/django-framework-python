from import_export import resources

from apps.sample.models import Book


class SampleResource(resources.ModelResource):
    class Meta:
        model = Book
