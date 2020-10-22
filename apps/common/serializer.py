from rest_framework import serializers


class DeleteSerialize(serializers.Serializer):
    pk = serializers.ListField(child=serializers.UUIDField(default=0))


class NoneSerializer(serializers.Serializer):
    pass
