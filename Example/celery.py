import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Example.settings')
app = Celery('Example')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.timezone = settings.TIME_ZONE

app.conf.beat_schedule = {
    'scheduled_send_chatwork-every-day': {
        'task': 'apps.chatbot.tasks.scheduled_send_chatwork',
        'schedule': crontab(hour=9, minute=0),
    },
    'scheduled_update_revenue-every-day': {
        'task': 'apps.shops.tasks.scheduled_update_revenue',
        'schedule': crontab(hour=0, minute=0),
    },
    'scheduled_test': {
        'task': 'apps.chatbot.tasks.test',
        'schedule': crontab(),
    }
}


app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('default', routing_key='default'),
    Queue('queue', routing_key='queue'),
)
