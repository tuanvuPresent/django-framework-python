# Create your views here.
from rest_framework.viewsets import ModelViewSet

from api.webhook.models import WebhookTarget
from api.webhook.serializer import WebhookTargetSerializer


class HookViewSet(ModelViewSet):
    queryset = WebhookTarget.objects.all()
    serializer_class = WebhookTargetSerializer
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
