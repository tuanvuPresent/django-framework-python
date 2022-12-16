from django.db import models
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.common.models import UuidModel
from apps.webhook.signals import raw_hook_event
from apps.webhook.tasks import deliver_hook_event

User = get_user_model()


class WebhookTarget(UuidModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.CharField(max_length=63)
    target_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "webhook"


@receiver(raw_hook_event)
def raw_custom_event(sender, event, payload, user, **kwargs):
    hooks = WebhookTarget.objects.filter(user=user, event=event)
    for hook in hooks:
        deliver_hook_event.delay(hook.target_url, payload)
