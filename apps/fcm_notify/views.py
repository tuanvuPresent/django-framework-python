from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.custom_model_view_set import BaseGenericViewSet
from apps.common.custom_permission import IsAdminUser
from apps.fcm_notify.serializer import SendNotifySerializer
from apps.fcm_notify.tasks import send_notify_message


class FcmNotifyAPIView(BaseGenericViewSet):
    serializer_action_classes = {
        'send_notify': SendNotifySerializer
    }
    permission_classes = [IsAdminUser]

    @action(methods=['POST'], detail=False)
    def send_notify(self, request):
        title = request.data.get('title')
        body = request.data.get('body')
        registration_id = request.data.get('registration_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_notify_message.delay(registration_id, title, body)
        return Response(data=None)
