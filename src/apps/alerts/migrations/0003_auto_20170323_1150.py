# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-03-23 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0002_auto_20170323_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertanuncio',
            name='estado_inmueble',
            field=models.CharField(blank=True, choices=[('OBRANUEVA', 'Obra nueva'), ('BUENESTADO', 'Buen estado'), ('AREFORMAR', 'A reformar')], default='', max_length=50, verbose_name='Estado'),
        ),
    ]
