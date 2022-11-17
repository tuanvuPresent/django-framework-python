import json

import requests
from celery import shared_task


@shared_task(name='deliver_hook_event')
def deliver_hook_event(target_url, payload):
    requests.post(
        url=target_url,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
