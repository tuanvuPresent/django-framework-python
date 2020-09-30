from rest_framework import serializers

from apps.upfile.constant import CSVUploadInfo


class CVSFileSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate(self, file):
        file = file['file']
        name_file = file.name
        size_file = file.size

        if size_file > CSVUploadInfo.LIMIT_SIZE.value:
            raise serializers.ValidationError('size file must < 2MB')

        if not (name_file.endswith('.csv')):
            raise serializers.ValidationError('wrong file format')

        return file
