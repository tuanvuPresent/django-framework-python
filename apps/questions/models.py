from django.db import models

from apps.common.models import BaseModel
from apps.exams.constant import LEVEL_CHOICE, KNOW, ANSWERS_CHOICE, ANSWER_A


# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=64)


class Question(BaseModel):
    content = models.TextField(max_length=1000)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='question_category')
    level = models.CharField(choices=LEVEL_CHOICE, default=KNOW, max_length=16)
    fix_answer = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    key = models.CharField(choices=ANSWERS_CHOICE, default=ANSWER_A, max_length=2)


class Answer(BaseModel):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.CharField(max_length=512)
    is_true = models.BooleanField(default=True)
