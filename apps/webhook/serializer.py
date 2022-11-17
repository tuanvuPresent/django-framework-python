from rest_framework import serializers

from api.webhook.models import WebhookTarget


class WebhookTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookTarget
        fields = ('id', 'target_url', 'event', 'user')
        read_only_fields = ('id', 'user')
