# Generated by Django 3.1.1 on 2020-10-07 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200914_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_verify_email',
            field=models.BooleanField(default=False),
        ),
    ]
