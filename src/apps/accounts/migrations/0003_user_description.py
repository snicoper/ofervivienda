# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-19 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170318_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Descripción'),
        ),
    ]
