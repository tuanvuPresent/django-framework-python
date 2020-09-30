from django.db import models

from apps.account.models import User
from apps.common.models import BaseModel
from apps.exams.constant import KNOW, LEVEL_CHOICE
from apps.questions.models import Question, Category


# Create your models here.
class Topic(BaseModel):
    name = models.CharField(max_length=64)


class ExamConfiguration(BaseModel):
    TEST = 'Test'
    PRACTICE = 'Practice'
    FROM_CHOICE = [
        (TEST, 'test'),
        (PRACTICE, 'practice')
    ]

    name = models.CharField(max_length=64, unique=True)
    quantity_question = models.IntegerField()
    time = models.TimeField()
    form = models.CharField(max_length=10, choices=FROM_CHOICE, default=TEST)
    recreate_question = models.BooleanField(default=True)
    show_random_question = models.BooleanField(default=True)


class Configuration(BaseModel):
    exam_config_id = models.ForeignKey(ExamConfiguration, on_delete=models.CASCADE, related_name='config')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    level = models.CharField(choices=LEVEL_CHOICE, default=KNOW, max_length=16)
    number = models.IntegerField()


class Exams(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=64, default=None)
    topic_id = models.ForeignKey(Topic, related_name='topic', on_delete=models.CASCADE)
    exam_config_id = models.ForeignKey(ExamConfiguration, related_name='exam_config', on_delete=models.CASCADE)
    question_id = models.ManyToManyField(Question, related_name="exam_question")


class HistoryExam(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history_exam_user')
    score = models.IntegerField()
    number_of_question_correct = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    exam_id = models.ForeignKey(Exams, on_delete=models.CASCADE, related_name='history_exam')
