from django.core.mail import send_mail
from django.conf import settings
from Example.celery import app

@app.task()
def send_mail_reset_password_v3(to_email, uid, token):
    link = str(settings.LINK_RESET_PASSWORD).format(uid, token)
    body = f'Xin chào {to_email} , \n\nBạn đã yêu cầu đặt lại mật khẩu cho tài khoản của bạn.\n\nNhấn vào liên kết dưới đây để đặt mật khẩu mới: {link}.\n\nAdmin,'
    send_mail('Đặt lại mật khẩu', body, '', [to_email], fail_silently=False)