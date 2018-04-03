# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 20:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0005_bookedplace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedplace',
            name='author',
            field=models.ForeignKey(db_column='author', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
