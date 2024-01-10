# Generated by Django 4.2.7 on 2024-01-06 21:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_followerscount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('recipe_id', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
                ('txt', models.CharField(default='None', max_length=400)),
            ],
        ),
    ]
