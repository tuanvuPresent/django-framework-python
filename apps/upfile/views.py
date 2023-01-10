from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.common.custom_model_view_set import BaseGenericViewSet
from apps.upfile.constant import ImageUploadInfo
from apps.upfile.handle_image import add_file
from apps.upfile.serializer import FileSerializer, FileStoreSerializer


class FileUploadView(BaseGenericViewSet):
    throttle_scope = 'upload'
    parser_classes = (MultiPartParser,)

    @action(methods=['POST'], detail=False, url_path='image')
    @swagger_auto_schema(request_body=FileSerializer)
    def post(self, request):
        file = request.FILES
        serializer = FileSerializer(data=file)
        serializer.is_valid(raise_exception=True)

        file = file['file']
        file_url = add_file(file, ImageUploadInfo.URL.value)
        file_url = request.build_absolute_uri(file_url)

        return Response(data=file_url)

class FileUploadViewSet(BaseGenericViewSet):
    throttle_scope = 'upload'
    parser_classes = (MultiPartParser,)
    serializer_action_classes = {
        'post_upload_file' : FileStoreSerializer
    }

    @action(methods=['POST'], detail=False, url_path='image')
    @swagger_auto_schema(request_body=FileStoreSerializer)
    def post_upload_file(self, request):
        file = request.FILES

        serializer = self.get_serializer(data=file)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)