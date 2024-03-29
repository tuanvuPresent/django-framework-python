from zipfile import BadZipFile
import pandas as pd
import openpyxl as openpyxl
from apps.common.constant import ErrorMessage
from apps.common.custom_exception_handler import CustomAPIException
from apps.common.custom_model_view_set import BaseGenericViewSet
from apps.import_file.serializer import CVSFileSerializer
from apps.upfile.serializer import FileSerializer
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


class ImportAPIView(BaseGenericViewSet):
    parser_classes = (MultiPartParser,)

    @action(methods=['POST'], detail=False, url_path='xlsx')
    @swagger_auto_schema(request_body=FileSerializer)
    def import_xlsx(self, request):
        excel_file = request.FILES["file"]
        try:
            wb = openpyxl.load_workbook(excel_file)
        except BadZipFile as e:
            raise CustomAPIException(ErrorMessage.FORMAT_FILE) from e

        excel_data = []
        for worksheet in wb:
            for row in worksheet.iter_rows():
                row_data = [str(cell.value) for cell in row]
                excel_data.append(row_data)

        return Response(data=excel_data)

    @action(methods=['POST'], detail=False, url_path='csv')
    @swagger_auto_schema(request_body=CVSFileSerializer)
    def import_csv(self, request):
        file = request.FILES
        serializer = CVSFileSerializer(data=file)
        serializer.is_valid(raise_exception=True)

        file = file['file']
        lines = file.read().decode('UTF-8').split('\n')
        lines.pop(len(lines) - 1)

        items = ['type', 'name', 'pass', 'No']
        data = []
        for line in lines:
            line = line.split(',')
            res = {str(item): line[col] for col, item in enumerate(items)}
            data.append(res)
        return Response(data=data)

    @action(methods=['post'], detail=False, url_path='csv-xlsx', parser_classes=[MultiPartParser, ])
    @swagger_auto_schema(request_body=CVSFileSerializer)
    @transaction.atomic()
    def import_csv_or_xlsx(self, request):
        file = request.FILES['file']
        try:
            if file.content_type == 'text/csv':
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        except:
            raise CustomAPIException()

        row_iter = df.iterrows()
        return Response()
