from rest_framework import serializers

from Example import settings
from apps.sample.todos.models import Todo


class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'title', 'description', 'date_start', 'date_end']
        model = Todo
        extra_kwargs = {
            'date_start': {'format': settings.FORMAT_DATETIME},
            'date_end': {'format': settings.FORMAT_DATETIME}
        }

    def validate(self, data):
        if data.get('date_start') > data.get('date_end'):
            raise serializers.ValidationError('data_start must < date_end')
        return data


class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'title', 'description', 'date_start', 'date_end']
        model = Todo
        extra_kwargs = {
            'date_start': {'format': settings.FORMAT_DATETIME},
            'date_end': {'format': settings.FORMAT_DATETIME}
        }

    def validate(self, data):
        if data.get('date_start') > data.get('date_end'):
            raise serializers.ValidationError('data_start must < date_end')
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user_id'] = request.user
        return super().create(validated_data)
