# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-10 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        ('article', '0003_auto_20180903_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='tag.Tag'),
        ),
    ]