# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-26 19:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20180831_2353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userstatistics',
            old_name='dislike_count',
            new_name='discussion_count',
        ),
        migrations.RemoveField(
            model_name='userstatistics',
            name='like_count',
        ),
    ]
