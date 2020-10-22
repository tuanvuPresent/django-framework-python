from django.core.mail import send_mail

from Example.celery import app


@app.task()
def send_mail_task(subject, body, to):
    send_mail(subject, body, '', [to], fail_silently=False)
