# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-18 19:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useroptions',
            name='email_public',
            field=models.BooleanField(default=False, verbose_name='Email público'),
        ),
        migrations.AlterField(
            model_name='useroptions',
            name='phone_public',
            field=models.BooleanField(default=False, verbose_name='Teléfono público'),
        ),
    ]