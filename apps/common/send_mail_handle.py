from django.core.mail import send_mail
from django.conf import settings


def send_mail_html(user_mail, subject, html_template):
    send_mail(
        subject,
        "",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_mail],
        html_message=html_template,
        fail_silently=True
    )
