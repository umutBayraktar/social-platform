# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-23 18:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20181018_0946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usernormal',
            name='interested_tags',
        ),
    ]