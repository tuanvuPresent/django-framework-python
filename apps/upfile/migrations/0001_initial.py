# Generated by Django 3.2 on 2022-12-16 08:02

import apps.upfile.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.FileField(upload_to=apps.upfile.models.directory_path)),
            ],
            options={
                'db_table': 'filestores',
            },
        ),
    ]
