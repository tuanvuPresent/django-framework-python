from django.db import models

from apps.common.models import UuidModel
from apps.e_learning.exams.constant import LevelQuestion, AnswersType


class Category(UuidModel):
    name = models.CharField(max_length=64)


class Question(UuidModel):
    content = models.TextField(max_length=1000)
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='question_category')
    level = models.IntegerField(
        choices=LevelQuestion.choices(), default=LevelQuestion.KNOW.value)
    fix_answer = models.BooleanField(default=True)
    key = models.IntegerField(
        choices=AnswersType.choices(), default=AnswersType.ANSWER_A.value)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class Answer(UuidModel):
    question_id = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    content = models.CharField(max_length=512)
    is_true = models.BooleanField(default=True)
