from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from apps.export_file.v2.export_service import ExportService


class ExportV2APIView(GenericViewSet):

    @action(methods=['GET'], detail=False, url_path='users-xlsx')
    def export_users_xls(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'
        response = ExportService().export(response)
        return response
