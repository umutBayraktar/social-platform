# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-07 11:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20181018_0946'),
        ('article', '0014_auto_20181207_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('link', models.URLField()),
                ('is_positive', models.BooleanField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_articles', to='article.Article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_articles', to='user.UserNormal')),
            ],
        ),
    ]