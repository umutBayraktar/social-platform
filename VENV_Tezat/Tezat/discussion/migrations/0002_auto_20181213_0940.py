# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-13 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discusion',
            name='video_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]