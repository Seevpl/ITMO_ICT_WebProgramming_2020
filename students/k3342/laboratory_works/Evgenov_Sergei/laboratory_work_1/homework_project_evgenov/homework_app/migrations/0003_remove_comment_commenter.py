# Generated by Django 3.0.5 on 2020-06-07 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homework_app', '0002_auto_20200607_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='commenter',
        ),
    ]
