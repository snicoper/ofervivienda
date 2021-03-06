# -*- coding: utf-8 -*-
# Generated by Django 1.11b1 on 2017-03-17 23:05
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(default='', max_length=100, verbose_name='País')),
                ('state', models.CharField(default='', max_length=100, verbose_name='Provincia')),
                ('city', models.CharField(default='', max_length=100, verbose_name='Población')),
                ('address', models.CharField(default='', max_length=200, verbose_name='Dirección')),
                ('zipcode', models.CharField(default='', max_length=100, verbose_name='Código postal')),
                ('location_string', models.CharField(blank=True, db_index=True, default='', max_length=255, verbose_name='Location string')),
                ('latitude', models.FloatField(blank=True, default=0, verbose_name='Latitud')),
                ('longitude', models.FloatField(blank=True, default=0, verbose_name='Longitud')),
                ('radius', models.IntegerField(blank=True, null=True, verbose_name='Radius')),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Point')),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326, verbose_name='Polígono')),
                ('category', models.CharField(choices=[('PISO', 'Piso'), ('CASA', 'Casa'), ('APARTAMENTO', 'Apartamento'), ('HABITACION', 'Habitacion'), ('TERRENO', 'Terreno'), ('PARKING', 'Parking'), ('INDUSTRIAL', 'Nave Industrial'), ('LOCAL', 'Local')], max_length=50, verbose_name='Categoría')),
                ('type_anuncio', models.CharField(choices=[('VENTA', 'Venta'), ('ALQUILER', 'Alquiler')], max_length=50, verbose_name='Tipo anuncio')),
                ('estado_inmueble', models.CharField(blank=True, choices=[('NUEVO', 'Nuevo'), ('SEGUNDAMANO', 'Segunda mano'), ('REFORMAS', 'Requiere reformas')], default='', max_length=50, verbose_name='Estado')),
                ('metros_cuadrados', models.PositiveIntegerField(blank=True, null=True, verbose_name='Metros cuadrados')),
                ('precio', models.DecimalField(blank=True, decimal_places=0, max_digits=7, null=True, verbose_name='Precio')),
                ('currency', models.CharField(choices=[('EUR', '€'), ('USD', '$'), ('GBP', '£')], default='EUR', max_length=3, verbose_name='Moneda')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('is_premium', models.BooleanField(default=False, verbose_name='Anuncio premium')),
                ('phone', models.CharField(blank=True, default='', max_length=20, verbose_name='Teléfono contacto')),
                ('description', models.TextField(blank=True, default='', verbose_name='Descripción')),
                ('views', models.IntegerField(blank=True, default=0, verbose_name='Visitas')),
                ('update_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha ultima modificación')),
            ],
            options={
                'ordering': ('-active', '-is_premium', '-update_at'),
            },
        ),
        migrations.CreateModel(
            name='AnuncioApartamento',
            fields=[
                ('anuncio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='anuncios.Anuncio')),
                ('habitaciones', models.PositiveSmallIntegerField(verbose_name='Habitaciones')),
                ('banos', models.PositiveSmallIntegerField(verbose_name='Baños')),
                ('ano_construccion', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Año de construcción')),
                ('parking', models.BooleanField(default=False, verbose_name='Plaza Parking')),
            ],
            options={
                'abstract': False,
            },
            bases=('anuncios.anuncio', models.Model),
        ),
        migrations.CreateModel(
            name='AnuncioCasa',
            fields=[
                ('anuncio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='anuncios.Anuncio')),
                ('habitaciones', models.PositiveSmallIntegerField(verbose_name='Habitaciones')),
                ('banos', models.PositiveSmallIntegerField(verbose_name='Baños')),
                ('ano_construccion', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Año de construcción')),
                ('parking', models.BooleanField(default=False, verbose_name='Plaza Parking')),
            ],
            options={
                'abstract': False,
            },
            bases=('anuncios.anuncio', models.Model),
        ),
        migrations.CreateModel(
            name='AnuncioHabitacion',
            fields=[
                ('anuncio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='anuncios.Anuncio')),
                ('permite_fumar_habitacion', models.BooleanField(default=False, verbose_name='Fumar en habitación')),
                ('permite_fumar_piso', models.BooleanField(default=False, verbose_name='Fumar en el piso')),
                ('internet', models.BooleanField(default=False, verbose_name='Conexión a Internet')),
            ],
            options={
                'abstract': False,
            },
            bases=('anuncios.anuncio', models.Model),
        ),
        migrations.CreateModel(
            name='AnuncioIndustrial',
            fields=[
                ('anuncio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='anuncios.Anuncio')),
            ],
            options={
                'abstract': False,
            },
            bases=('anuncios.anuncio', models.Model),
        ),
        migrations.CreateModel(
            name='AnuncioLocal',
            fields=[
                ('anuncio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='anuncios.Anuncio')),
            ],
            options={
                'abstract': False,
            },
            bases=('anuncios.anuncio', models.Model),
        ),
        migrations.CreateModel(
            name='AnuncioParking',
            fields=[
                ('anuncio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='anuncios.Anuncio')),
            ],
            options={
                'abstract': False,
            },
            bases=('anuncios.anuncio', models.Model),
        ),
        migrations.CreateModel(
            name='AnuncioPiso',
            fields=[
                ('anuncio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='anuncios.Anuncio')),
                ('habitaciones', models.PositiveSmallIntegerField(verbose_name='Habitaciones')),
                ('banos', models.PositiveSmallIntegerField(verbose_name='Baños')),
                ('ano_construccion', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Año de construcción')),
                ('parking', models.BooleanField(default=False, verbose_name='Plaza Parking')),
            ],
            options={
                'abstract': False,
            },
            bases=('anuncios.anuncio', models.Model),
        ),
        migrations.CreateModel(
            name='AnuncioTerreno',
            fields=[
                ('anuncio_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='anuncios.Anuncio')),
            ],
            options={
                'abstract': False,
            },
            bases=('anuncios.anuncio', models.Model),
        ),
        migrations.AddField(
            model_name='anuncio',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anuncios_owner', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]
