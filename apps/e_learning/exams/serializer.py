from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from Example import settings
from apps.e_learning.exams.constant import AnswersType
from apps.e_learning.models.exam import Exams, ExamConfiguration, Topic, Configuration, HistoryExam
from apps.e_learning.exams.utils import get_question
from apps.e_learning.models.question import Question
from apps.e_learning.questions.serializer import AnswerSerializer
from apps.e_learning.config_question.serializer import ListExamConfigSerializer

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name']
        model = Topic


class ListExamSerializer(serializers.ModelSerializer):
    topic_id = TopicSerializer()
    exam_config_id = ListExamConfigSerializer()

    class Meta:
        fields = ['id', 'name', 'description',
                  'topic_id', 'exam_config_id']
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
            name=name_topic)
        return Exams.objects.create(topic_id=topic, **validated_data)

    def update(self, instance, validated_data):
        topic_id = validated_data.pop('topic_id')
        name_topic = topic_id.get('name')
        topic, is_created = Topic.objects.get_or_create(
            name=name_topic)
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
        fields = ['name', 'description', 'topic_id', 'questions']
        model = Exams


class ChildDoExamSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    key = serializers.ChoiceField(choices=AnswersType.choices())


class DoExamSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()
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
    question = serializers.IntegerField()
    key = serializers.ChoiceField(choices=AnswersType.choices())
    is_correct = serializers.BooleanField(default=False)
    your_answer = serializers.ChoiceField(choices=AnswersType.choices())


class DetailResultDoExamSerializer(serializers.Serializer):
    result = HistoryExamSerialize()
    detail = ResultDoExamSerializer(many=True)
