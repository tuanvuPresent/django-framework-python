from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Phone(models.Model):
    security_code = models.CharField(max_length=64)
    session_token = models.CharField(max_length=500)
    phone_number = PhoneNumberField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.phone_number)
