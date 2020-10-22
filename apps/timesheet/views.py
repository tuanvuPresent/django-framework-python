from django.db import transaction
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.common.custom_model_view_set import BaseModelViewSet
from apps.common.custom_permission import IsAdminUser, IsAdminUserOrIsUserObjects
from apps.common.serializer import DeleteSerialize
from apps.timesheet.models import TimeSheet
from apps.timesheet.serializer import TimeSheetSerializer


# Create your views here.
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class TimeSheetAPIView(BaseModelViewSet):
    serializer_method_classes = {
        'GET': TimeSheetSerializer,
        'POST': TimeSheetSerializer,
        'DELETE': TimeSheetSerializer,
        'PUT': TimeSheetSerializer,
        'PATCH': TimeSheetSerializer
    }
    permission_action_classes = {
        'create': [IsAdminUser],
        'list': [IsAdminUser],
        'retrieve': [IsAdminUserOrIsUserObjects],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser]
    }

    def get_queryset(self):
        return TimeSheet.objects.filter(is_active=True)

    @transaction.atomic()
    @swagger_auto_schema(request_body=DeleteSerialize)
    @action(methods=['DELETE'], detail=False)
    def delete(self, request):
        pk = request.data['pk']
        timesheet = TimeSheet.objects.filter(is_active=True, id__in=pk)
        if timesheet.count() != len(pk):
            raise NotFound()

        timesheet.update(is_active=False)

        return Response()
