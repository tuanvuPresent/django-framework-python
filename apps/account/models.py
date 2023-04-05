import random

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.conf import settings
from apps.account.constant import GenderType, UserType
from apps.common.models import UuidModel


class User(UuidModel, AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True, null=True)
    user_type = models.IntegerField(
        choices=UserType.choices(), default=UserType.STAFF.value)
    is_staff = models.BooleanField(default=False)
    gender = models.IntegerField(
        choices=GenderType.choices(), default=GenderType.MALE.value)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verify_email = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def make_random_password(self, length=8,
                             allowed_chars="abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*"):
        return "".join(random.sample(allowed_chars, length))

    def save(self, *args, **kwargs):
        if self.email == "":
            self.email = None
        super(User, self).save(*args, **kwargs)


class UserProfile(UuidModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField()
    address = models.CharField(max_length=255)
    
    
class UserApiPermission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    api_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'auth_user_api_permission'


class GroupApiPermission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    api_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'auth_group_api_permission'
