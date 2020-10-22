import uuid

from django.db import models
from django.utils.timezone import now


class BaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, deleted_at=None)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = BaseManager()

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.deleted_at = now()
        self.save()

    class Meta:
        abstract = True
