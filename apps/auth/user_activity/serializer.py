from rest_framework import serializers

from apps.auth.jwt.models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ('id', 'session_key', 'created_at')


class LogoutDeviceOthersSerializer(serializers.Serializer):
    session_key = serializers.CharField()
