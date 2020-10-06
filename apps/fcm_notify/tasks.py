from fcm_django.models import FCMDevice

from Example.celery import app


@app.task()
def send_notify_message(registration_id, title, body):
    devices = FCMDevice.objects.filter(registration_id=registration_id)
    devices.send_message(title=title, body=body)
