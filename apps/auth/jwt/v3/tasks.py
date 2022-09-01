from django.core.mail import send_mail
from django.conf import settings
from Example.celery import app

@app.task()
def send_mail_reset_password_v3(to_email, uid, token):
    link = str(settings.LINK_RESET_PASSWORD).format(uid, token)
    body = 'Xin chào {} , \n\n' \
           'Bạn đã yêu cầu đặt lại mật khẩu cho tài khoản của bạn.\n\n' \
           'Nhấn vào liên kết dưới đây để đặt mật khẩu mới: {}.\n\n' \
           'Admin,'.format(to_email, link)
    send_mail('Đặt lại mật khẩu', body, '', [to_email], fail_silently=False)