import uuid

from django.db import models
from django.utils.timezone import now
from apps.common.uuid_gen import UuidGenSingletonGroup

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


class UuidModel(models.Model):

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.id = UuidGenSingletonGroup(self.__class__).gen()
        super(UuidModel, self).save(True, force_update, using, update_fields)

    class Meta:
        abstract = True