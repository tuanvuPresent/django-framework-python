# Generated by Django 2.2.8 on 2020-06-04 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0002_timesheet_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]