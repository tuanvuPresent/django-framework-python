from django.core.mail import send_mail
from django.conf import settings
from Example.celery import app


def send_mail_html(user_mail, subject, html_template):
    send_mail(
        subject,
        "",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_mail],
        html_message=html_template,
        fail_silently=True
    )


@app.task()
def send_mail_reset_password(mail, new_password):
    send_mail('reset password',
              'new password is {}'.format(new_password),
              '',
              [mail],
              fail_silently=False)


@app.task()
def send_mail_reset_password_v2(to_email, code):
    body = 'Xin chào {} , \n\n' \
           'Mã xác minh: {}\n' \
           'Mã này chỉ được sử dụng một lần và sẽ hết hạn trong vòng {} phút.\n\n' \
           'Admin,'.format(to_email, code, settings.RESET_PASSWORD_CODE_EXPIRATION_TIME / 60)
    send_mail('Đặt lại mật khẩu', body, '', [to_email], fail_silently=False)


@app.task()
def send_mail_reset_password_v3(to_email, uid, token):
    link = str(settings.LINK_RESET_PASSWORD).format(uid, token)
    body = 'Xin chào {} , \n\n' \
           'Bạn đã yêu cầu đặt lại mật khẩu cho tài khoản của bạn.\n\n' \
           'Nhấn vào liên kết dưới đây để đặt mật khẩu mới: {}.\n\n' \
           'Admin,'.format(to_email, link)
    send_mail('Đặt lại mật khẩu', body, '', [to_email], fail_silently=False)