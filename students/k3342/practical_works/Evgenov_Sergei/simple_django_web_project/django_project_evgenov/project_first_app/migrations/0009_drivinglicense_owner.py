# Generated by Django 3.0.5 on 2020-06-09 22:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_first_app', '0008_auto_20200610_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='drivinglicense',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
