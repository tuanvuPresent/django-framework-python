# Generated by Django 2.2.8 on 2020-05-26 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='deleted_at',
            field=models.DateTimeField(null=True),
        ),
    ]
