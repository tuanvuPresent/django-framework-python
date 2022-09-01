from rest_framework import serializers

from Example import settings
from apps.e_learning.exams.models import Category
from apps.e_learning.questions.constant import AnswerNumber
from apps.e_learning.questions.models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content']


class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content', 'is_true']
        read_only_fields = ['is_active']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name']
        model = Category


class CreateQuestionSerializer(serializers.ModelSerializer):
    category_id = CategorySerializer()
    answers = CreateAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'content', 'level', 'fix_answer', 'is_active', 'date_create', 'category_id', 'answers', 'key']
        read_only_fields = ['date_create', 'is_active']
        extra_kwargs = {
            'date_create': {'format': settings.FORMAT_DATETIME}
        }

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        category_id = validated_data.pop('category_id')
        name_category = category_id.get('name')

        category, is_create = Category.objects.get_or_create(name=name_category, is_active=True)
        question = Question.objects.create(category_id=category, **validated_data)

        # CACH 1:
        answer_list = [Answer(question_id=question, **answer) for answer in answers]
        Answer.objects.bulk_create(answer_list)
        # CACH 2:
        # for count, answer in enumerate(answers):
        #     Answer.objects.create(question_id=question, **answer)
        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers', instance.answers)
        category_id = validated_data.pop('category_id', instance.category_id)

        name_category = category_id.get('name')
        category, is_create = Category.objects.get_or_create(name=name_category, is_active=True)
        instance = super().update(instance, validated_data)
        instance.category_id = category

        # CACH 1:
        # answers = instance.answers.all()
        # answers = list(answers)
        # for ans_data in answers_data:
        #     try:
        #         answer = answers.pop(0)
        #         answer.content = ans_data.get('content', answer.content)
        #         answer.is_true = ans_data.get('is_true', answer.is_true)
        #         answer.save()
        #     except IndexError:
        #         Answer.objects.create(question_id=instance, **ans_data)
        # while len(answers):
        #     answer = answers.pop(0)
        #     answer.is_active = False
        #     answer.save()

        # CACH 2
        Answer.objects.filter(question_id=instance).delete()
        answer_list = [Answer(question_id=instance, **answer) for answer in answers_data]
        Answer.objects.bulk_create(answer_list)

        instance.save()
        return instance

    def validate_content(self, content):
        if len(content) < 6:
            raise serializers.ValidationError('length content must >= 6')

        if len(content) > 1000:
            raise serializers.ValidationError('length content must <= 1000')

        request = self.context.get('request')
        if request.method == 'POST' and Question.objects.filter(is_active=True, content=content.strip()):
            raise serializers.ValidationError('questions with this content already exists.')

        if request.method == 'PUT' and Question.objects.exclude(id=self.instance.pk).filter(is_active=True,
                                                                                            content=content.strip()):
            raise serializers.ValidationError('questions with this content already exists.')

        return content

    def validate_answers(self, answers):
        if len(answers) > AnswerNumber.MAX.value:
            raise serializers.ValidationError('{} {}'.format('number answer must <= ', AnswerNumber.MAX.value))

        if len(answers) < AnswerNumber.MIN.value:
            raise serializers.ValidationError('{} {}'.format('number answer must >= ', AnswerNumber.MIN.value))

        for answer in answers:
            if len(answer['content']) < 5:
                raise serializers.ValidationError('answer with this length content must >= 5.')

            if len(answer['content']) > 511:
                raise serializers.ValidationError('answer with this length content must <= 511')

        for answer in answers:
            if answer['is_true']:
                return answers

        raise serializers.ValidationError('question must be at least 1 correct answer')


class ListQuestionSerializer(serializers.ModelSerializer):
    category_id = CategorySerializer()
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'content', 'level', 'category_id', 'fix_answer', 'is_active', 'date_create', 'date_update',
                  'answers', 'key']
        read_only_fields = ['date_create', 'is_active']
        extra_kwargs = {
            'date_create': {'format': settings.FORMAT_DATETIME},
            'date_update': {'format': settings.FORMAT_DATETIME}
        }
