from django.db import models
import random
import string
import time
from django.utils.baseconv import base62

# Create your models here.
def directory_path(instance, filename):
    stamp = int(time.time() * 1000)
    return f'{"".join(random.choices(string.ascii_uppercase + string.digits, k=24))}' \
           f'{base62.encode(stamp)}.{filename.split(".")[1]}'


class FileStore(models.Model):
    url = models.FileField(upload_to=directory_path)

    class Meta:
        db_table = 'filestores'