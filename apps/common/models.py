import uuid

from django.db import models
from django.utils.timezone import now
from apps.common.uuid_gen import UuidGenSingletonGroup


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class AllSoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.save()

    class Meta:
        abstract = True


class UuidModel(models.Model):

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.id = UuidGenSingletonGroup(self.__class__).gen()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True
