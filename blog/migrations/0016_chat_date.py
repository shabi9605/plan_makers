# Generated by Django 3.2.7 on 2021-10-18 09:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
