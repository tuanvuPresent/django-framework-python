# Generated by Django 3.2 on 2022-11-22 10:51

import apps.upfile.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upfile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filestore',
            name='url',
            field=models.FileField(upload_to=apps.upfile.models.directory_path),
        ),
    ]
