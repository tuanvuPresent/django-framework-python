import random

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.account.constant import GENDER_CHOICES, MALE, USER_TYPE, STAFF
from apps.common.models import BaseModel


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True, null=True)
    user_type = models.CharField(choices=USER_TYPE, default=STAFF, max_length=8)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, default=MALE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verify_email = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def make_random_password(self, length=8,
                             allowed_chars="abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*"):
        new_password = "".join(random.sample(allowed_chars, length))
        return new_password

    def save(self, *args, **kwargs):
        if self.email == "":
            self.email = None
        super(User, self).save(*args, **kwargs)


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField()
    address = models.CharField(max_length=255)
