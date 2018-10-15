# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-03-24 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0005_auto_20170324_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alerthabitacion',
            name='genero',
            field=models.CharField(choices=[('CHICOCHICA', 'Chicos y Chicas'), ('CHICO', 'Chicos'), ('CHICA', 'Chicas')], default='CHICOCHICA', max_length=20, verbose_name='Genero'),
        ),
    ]
