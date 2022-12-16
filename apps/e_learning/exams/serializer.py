from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Example import settings
from apps.e_learning.exams.constant import AnswersType
from apps.e_learning.exams.models import Exams, ExamConfiguration, Topic, Configuration, HistoryExam
from apps.e_learning.exams.utils import get_question
from apps.e_learning.questions.models import Question
from apps.e_learning.questions.serializer import AnswerSerializer


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name']
        model = Topic


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['category_id', 'level', 'number']
        model = Configuration


class ListExamConfigSerializer(serializers.ModelSerializer):
    config = ConfigurationSerializer(many=True)

    class Meta:
        fields = ['id', 'name', 'quantity_question', 'time', 'form', 'recreate_question', 'show_random_question',
                  'is_active',
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
                is_active=True, category_id__name=category.name, level=level).count()
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


class ListExamSerializer(serializers.ModelSerializer):
    topic_id = TopicSerializer()
    exam_config_id = ListExamConfigSerializer()

    class Meta:
        fields = ['id', 'name', 'description',
                  'topic_id', 'exam_config_id', 'is_active']
        model = Exams


class CreateExamSerializer(serializers.ModelSerializer):
    topic_id = TopicSerializer()

    class Meta:
        fields = ['name', 'description', 'topic_id', 'exam_config_id']
        model = Exams

    def create(self, validated_data):
        topic_id = validated_data.pop('topic_id')
        name_topic = topic_id.get('name')
        topic, is_created = Topic.objects.get_or_create(
            name=name_topic, is_active=True)
        exam = Exams.objects.create(topic_id=topic, **validated_data)
        return exam

    def update(self, instance, validated_data):
        topic_id = validated_data.pop('topic_id')
        name_topic = topic_id.get('name')
        topic, is_created = Topic.objects.get_or_create(
            name=name_topic, is_active=True)
        instance = super().update(instance, validated_data)
        instance.topic_id = topic
        instance.save()

        return instance


# ----------------------------- Do exam ----------------------------------------------
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        fields = ['id', 'content', 'answers']
        model = Question


class ListDoExamSerializer(serializers.ModelSerializer):
    topic_id = TopicSerializer()
    questions = serializers.SerializerMethodField()

    def get_questions(self, data):
        questions = get_question(data)
        serializer = QuestionSerializer(questions, many=True)
        return serializer.data

    class Meta:
        fields = ['name', 'description', 'topic_id', 'is_active', 'questions']
        model = Exams


class ChildDoExamSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    key = serializers.ChoiceField(choices=AnswersType.choices())


class DoExamSerializer(serializers.Serializer):
    exam_id = serializers.UUIDField()
    answers = serializers.ListField(child=ChildDoExamSerializer())


class HistoryExamSerialize(serializers.ModelSerializer):
    number_question = serializers.SerializerMethodField('get_number')
    score = serializers.SerializerMethodField('get_score')

    def get_number(self, instance):
        return instance.exam_id.exam_config_id.quantity_question

    def get_score(self, instance):
        return instance.score / instance.exam_id.exam_config_id.quantity_question * 10

    class Meta:
        fields = ['user_id', 'date', 'exam_id',
                  'number_of_question_correct', 'number_question', 'score']
        model = HistoryExam
        extra_kwargs = {
            'date': {'format': settings.FORMAT_DATETIME}
        }


class ResultDoExamSerializer(serializers.Serializer):
    question = serializers.UUIDField()
    key = serializers.ChoiceField(choices=AnswersType.choices())
    is_correct = serializers.BooleanField(default=False)
    your_answer = serializers.ChoiceField(choices=AnswersType.choices())


class DetailResultDoExamSerializer(serializers.Serializer):
    result = HistoryExamSerialize()
    detail = ResultDoExamSerializer(many=True)
