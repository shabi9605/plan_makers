# Generated by Django 3.2.4 on 2021-06-18 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='user_name',
            new_name='name',
        ),
    ]