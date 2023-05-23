from django.core.mail import send_mail
from Example.celery import app


@app.task()
def send_mail_reset_password(mail, new_password):
    send_mail(
        'reset password',
        f'new password is {new_password}',
        '',
        [mail],
        fail_silently=False,
    )
