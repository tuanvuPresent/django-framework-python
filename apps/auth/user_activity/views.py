from rest_framework.permissions import IsAuthenticated
from apps.auth.jwt.models import UserActivity
from apps.auth.user_activity.serializer import UserActivitySerializer, LogoutDeviceOthersSerializer
from apps.common.custom_model_view_set import BaseGenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action


class UserActivityAPIView(BaseGenericViewSet,
                          mixins.ListModelMixin):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    serializer_action_classes = {
        'list': UserActivitySerializer,
        'logout_othes_device_others': LogoutDeviceOthersSerializer
    }

    @action(methods=['POST'], detail=False, url_path='logout-device-others')
    def logout_device_others(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_logout_device_others.send(sender=request.user.__class__, sid=request.data.get('session_key'))
        return Response()
