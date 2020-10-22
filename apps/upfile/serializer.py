from rest_framework import serializers

from apps.upfile.constant import ImageUploadInfo


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate(self, file):
        file = file['file']
        name_file = file.name
        size_file = file.size

        if size_file > ImageUploadInfo.LIMIT_SIZE.value:
            raise serializers.ValidationError('size file must < 2MB')

        if not any(name_file.endswith(suffix) for suffix in ImageUploadInfo.TYPE.value):
            raise serializers.ValidationError('wrong file format')

        return file
