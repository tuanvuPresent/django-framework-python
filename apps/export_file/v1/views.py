import csv
from textwrap import wrap

import xlwt as xlwt
from apps.account.models import User
from apps.common.serializer import NoneSerializer
from apps.e_learning.models.question import Question
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


class ExportAPIView(GenericViewSet):
    serializer_class = NoneSerializer

    @action(methods=['GET'], detail=False, url_path='users-xlsx')
    def export_users_xls(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['pk', 'username', 'first_name',
                   'last_name', 'gender', 'password']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = User.objects.all().values_list('pk', 'username', 'first_name',
                                              'last_name', 'gender', 'password')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response

    @action(methods=['get'], detail=False, url_path='users-csv')
    def export_users_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(['Username', 'First name',
                         'Last name', 'Email address'])

        users = User.objects.all().values_list(
            'username', 'first_name', 'last_name', 'email')
        for user in users:
            writer.writerow(user)

        return response

    @action(methods=['get'], detail=False, url_path='xlsx')
    def export_xlsx(self, request):
        data = {
            'Column 1': [],
            'Column 2': [],
        }
        file_name = 'effort.xlsx'
        df = pd.DataFrame(data)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=""{file_name}'
        df.to_excel(response, index=False)
        return response


class ExportPdfV1APIView(GenericViewSet):
    serializer_class = NoneSerializer

    @action(methods=['GET'], detail=False, url_path='download')
    def write_pdf_1(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

        p = canvas.Canvas(response)
        p.drawString(100, 100, "Hello world.")
        p.showPage()
        p.save()

        return response


class ExportPdfV2APIView(GenericViewSet):
    serializer_class = NoneSerializer

    @action(methods=['GET'], detail=False, url_path='download')
    def write_pdf_2(self, request):
        doc = SimpleDocTemplate("/tmp/download.pdf", pagesizes=A4)
        styles = getSampleStyleSheet()
        Story = []
        style = styles["Normal"]
        for i in range(10):
            bogustext = (
                f"This is This number This is This numberThis is This numberThis is This numberThis is This numberThis is This numberThis is This numberThis is This numberThis is This numberThis is This numberThis is This numberThis is This number {i}.  ---- "
                * 20
            )
            p = Paragraph(bogustext, style)
            Story.extend((p, Spacer(1, 0.2 * inch)))
        doc.build(Story)

        fs = FileSystemStorage("/tmp")
        with fs.open("download.pdf") as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="download.pdf"'
            return response


class ExportPdfV3APIView(GenericViewSet):
    serializer_class = NoneSerializer

    @action(methods=['GET'], detail=False, url_path='download')
    def write_pdf_3(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="download.pdf"'

        pdf = canvas.Canvas(response)
        pdf.setTitle('Title')
        pdf.drawString(200, 800, 'DANH SACH CAU HOI')
        question = Question.objects.prefetch_related('answers')
        x = 40
        y = 750
        for _ in range(10):
            for item in question:
                pdf.drawString(x, y, f'{item.content}:')
                y -= 15
                if y < 40:
                    pdf.showPage()
                    y = 800
                for index, answer in enumerate(item.answers.all()):
                    pdf.drawString(x, y, f'    {str(index)}.{answer.content}')
                    y -= 15
                    if y < 40:
                        pdf.showPage()
                        y = 800

        text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. " \
                   "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, " \
                   "when an unknown printer took a galley of type and scrambled it to make a type specimen book."
        t = pdf.beginText(40, 800)
        wraped_text = "\n".join(wrap(text, 80))  # 80 is line width
        pdf.showPage()
        t.textLines(wraped_text)
        pdf.drawText(t)

        pdf.save()
        return response
