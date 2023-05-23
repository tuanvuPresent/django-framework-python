from Example.celery import app
from apps.account.models import User
import xlwt as xlwt
from apps.export_file.models import DownloadFileLog


def get_path():
    pass


@app.task()
def export_user(ws):
    instance = DownloadFileLog.objects.create(name='download user xlsx')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['pk', 'username', 'first_name', 'last_name', 'gender', 'password']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = User.objects.all().values_list('pk', 'username', 'first_name', 'last_name', 'gender', 'password')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    instance.path = get_path()
    instance.status = DownloadFileLog.StatusType.SUCCESS.value
    instance.save()
