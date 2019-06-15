# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-08-19 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statictics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_count', models.IntegerField(default=0)),
                ('dislike_count', models.IntegerField(default=0)),
                ('positive_comment', models.IntegerField(default=0)),
                ('negative_comment', models.IntegerField(default=0)),
                ('pageview', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='pageview',
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Resim'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.TextField(blank=True, null=True, verbose_name='Etiketler'),
        ),
        migrations.AddField(
            model_name='article',
            name='statistics',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='article.Statictics'),
            preserve_default=False,
        ),
    ]