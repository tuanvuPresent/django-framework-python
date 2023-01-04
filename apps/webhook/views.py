from rest_framework.viewsets import ModelViewSet

from apps.webhook.models import WebhookTarget
from apps.webhook.serializer import WebhookTargetSerializer


class HookViewSet(ModelViewSet):
    queryset = WebhookTarget.objects.all()
    serializer_class = WebhookTargetSerializer
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
