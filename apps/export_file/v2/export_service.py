import xlwt as xlwt
from apps.export_file.tasks import export_user

class ExportService:

    def export(self, response):
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        export_user.delay(ws)
        wb.save(response)
        return response