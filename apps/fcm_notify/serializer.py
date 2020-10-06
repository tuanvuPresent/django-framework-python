from rest_framework import serializers


class SendNotifySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=32, required=True)
    body = serializers.CharField(max_length=512, required=True)
    registration_id = serializers.CharField(max_length=216, required=True)
