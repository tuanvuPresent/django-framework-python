from django.db import transaction
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from apps.export_file.v3.resource import SampleResource


class SampleExportApiView(GenericViewSet):

    @action(methods=['POST'], detail=False, url_path='csv')
    @transaction.atomic
    def export_csv(self, request, *args, **kwargs):
        book_resource = SampleResource()
        data = book_resource.export()
        response = HttpResponse(data.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books.csv"'
        return response
