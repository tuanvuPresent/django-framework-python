from django.core.mail import send_mail
from django.conf import settings
from Example.celery import app

@app.task()
def send_mail_reset_password_v2(to_email, code):
    body = f'Xin chào {to_email} , \n\nMã xác minh: {code}\nMã này chỉ được sử dụng một lần và sẽ hết hạn trong vòng {settings.RESET_PASSWORD_CODE_EXPIRATION_TIME / 60} phút.\n\nAdmin,'
    send_mail('Đặt lại mật khẩu', body, '', [to_email], fail_silently=False)


