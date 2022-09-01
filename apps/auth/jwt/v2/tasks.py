from django.core.mail import send_mail
from django.conf import settings
from Example.celery import app

@app.task()
def send_mail_reset_password_v2(to_email, code):
    body = 'Xin chào {} , \n\n' \
           'Mã xác minh: {}\n' \
           'Mã này chỉ được sử dụng một lần và sẽ hết hạn trong vòng {} phút.\n\n' \
           'Admin,'.format(to_email, code, settings.RESET_PASSWORD_CODE_EXPIRATION_TIME / 60)
    send_mail('Đặt lại mật khẩu', body, '', [to_email], fail_silently=False)


