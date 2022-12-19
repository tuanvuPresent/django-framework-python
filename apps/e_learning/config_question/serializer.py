from apps.e_learning.models.exam import ExamConfiguration, Configuration
from apps.e_learning.models.question import Question
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['category_id', 'level', 'number']
        model = Configuration


class ListExamConfigSerializer(serializers.ModelSerializer):
    config = ConfigurationSerializer(many=True)

    class Meta:
        fields = ['id', 'name', 'quantity_question', 'time', 'form', 'recreate_question', 'show_random_question',
                  'config']
        model = ExamConfiguration


class CreateExamConfigSerializer(serializers.ModelSerializer):
    config = ConfigurationSerializer(many=True)

    class Meta:
        fields = ['name', 'quantity_question', 'time', 'form', 'recreate_question', 'show_random_question',
                  'config']
        model = ExamConfiguration

    def validate(self, data):
        config_data = data.get('config')
        quantity = 0
        for config_item in config_data:
            quantity = quantity + config_item.get('number')
            category = config_item.get('category_id')
            level = config_item.get('level')
            number = Question.objects.filter(
                category_id__name=category.name, level=level).count()
            if number < config_item.get('number'):
                raise ValidationError(
                    'The number of questions for category {}, level {} cannot be more than {}'.format(
                        category.pk, level, number)
                )

        if quantity != data.get('quantity_question'):
            raise ValidationError(
                'quantity_question = {} is invalid'.format(
                    data.get('quantity_question'))
            )
        return data

    def validate_config(self, data):
        fields = ['category_id', 'level']
        data_copy = []
        for e in data:
            temp = {}
            for k, v in e.items():
                if k in fields:
                    temp[k] = v
            data_copy.append(temp)

        list_config = []
        for item in data_copy:
            if item not in list_config:
                list_config.append(item)

        if len(data) != len(list_config):
            raise ValidationError(
                'exam configuration with this level and category already exists.')
        return data

    def create(self, validated_data):
        configuration_data = validated_data.pop('config')
        exam_config = ExamConfiguration.objects.create(**validated_data)

        config_list = [Configuration(exam_config_id=exam_config, **configuration) for configuration in
                       configuration_data]
        Configuration.objects.bulk_create(config_list)

        return exam_config

    def update(self, instance, validated_data):
        config_data = validated_data.pop('config', instance.config)
        instance = super().update(instance, validated_data)

        Configuration.objects.filter(exam_config_id=instance).delete()
        config_list = [Configuration(
            exam_config_id=instance, **config_item) for config_item in config_data]
        Configuration.objects.bulk_create(config_list)

        instance.save()
        return instance
