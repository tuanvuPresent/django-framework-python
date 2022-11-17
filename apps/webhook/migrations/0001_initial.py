# Generated by Django 3.2.16 on 2022-11-17 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WebhookTarget',
            fields=[
                ('id', models.BigIntegerField(default=None, primary_key=True, serialize=False)),
                ('event', models.CharField(max_length=63)),
                ('target_url', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'webhook',
            },
        ),
    ]
