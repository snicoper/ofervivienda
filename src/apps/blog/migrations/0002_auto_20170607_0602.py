# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 04:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-create_at',), 'verbose_name': 'Articulo', 'verbose_name_plural': 'artículos'},
        ),
        migrations.AlterModelOptions(
            name='articlesubscribe',
            options={'verbose_name': 'Subscrito a artículos', 'verbose_name_plural': 'Subscritos a artículos'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('-views',), 'verbose_name': 'Etiqueta', 'verbose_name_plural': 'Etiquetas'},
        ),
        migrations.AlterField(
            model_name='article',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(verbose_name='Cuerpo'),
        ),
        migrations.AlterField(
            model_name='article',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación'),
        ),
        migrations.AlterField(
            model_name='article',
            name='default_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_default_tag', to='blog.Tag', verbose_name='Etiqueta principal'),
        ),
        migrations.AlterField(
            model_name='article',
            name='image_header',
            field=models.ImageField(blank=True, null=True, upload_to='articles/headers', verbose_name='Imagen cabecera'),
        ),
        migrations.AlterField(
            model_name='article',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_owner', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(related_name='article_tags', to='blog.Tag', verbose_name='Etiquetas'),
        ),
        migrations.AlterField(
            model_name='article',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha modificación'),
        ),
        migrations.AlterField(
            model_name='article',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Vistas'),
        ),
        migrations.AlterField(
            model_name='articlesubscribe',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='articlesubscribe',
            name='token_unsigned',
            field=models.CharField(max_length=30, unique=True, verbose_name='Token unregister'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='thumbnail',
            field=models.ImageField(upload_to='articles/tags', verbose_name='Miniatura'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='views',
            field=models.IntegerField(default=0, verbose_name='Vistas'),
        ),
    ]
