# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-30 09:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0010_auto_20181012_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='article.Comment'),
        ),
    ]
