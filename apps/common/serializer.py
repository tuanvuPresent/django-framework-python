from rest_framework import serializers


class DeleteSerialize(serializers.Serializer):
    pk = serializers.ListField(child=serializers.IntegerField(default=0))


class NoneSerializer(serializers.Serializer):
    pass
