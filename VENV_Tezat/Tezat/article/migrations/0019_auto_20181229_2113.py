# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-29 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0018_auto_20181223_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='article', to='tag.Tag'),
        ),
    ]
