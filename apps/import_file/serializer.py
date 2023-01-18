from rest_framework import serializers


class CVSFileSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate(self, file):
        file = file['file']
        name_file = file.name
        size_file = file.size

        if not (name_file.endswith('.csv')):
            raise serializers.ValidationError('wrong file format')

        return file
