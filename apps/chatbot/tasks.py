from datetime import datetime

from Example.celery import app
from apps.chatbot.handle_chatbot import send_chatwork, get_weather, get_xskt


@app.task()
def scheduled_send_chatwork():
    send_chatwork(get_xskt(), 'KQXS')
    send_chatwork(get_weather(), 'Weather')


@app.task()
def test():
    now = datetime.now()
    f = open("schedule_test.txt", "a")
    f.write('\n' + str(now))
    f.close()
