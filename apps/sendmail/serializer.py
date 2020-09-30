from rest_framework import serializers


class SendEmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=64)
    message = serializers.CharField(max_length=64)
    to_email = serializers.CharField(max_length=64)
    # file = serializers.FileField()
