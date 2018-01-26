# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-26 10:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(help_text='codigo del almacen', max_length=32, unique=True)),
                ('nombre', models.CharField(help_text='nombre del almacen', max_length=30)),
                ('direccion', models.CharField(help_text='direccion del almacen', max_length=60)),
                ('telefono', models.CharField(help_text='telefono de comunicacion', max_length=15, null=True)),
                ('eliminable', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='nombre del almacen', max_length=30)),
                ('volumen_restante', models.FloatField(default=0, help_text='capacidad disponible en el almacen')),
                ('longitud', models.FloatField(help_text='longitud del almacen')),
                ('anchura', models.FloatField(help_text='anchura del almacen')),
                ('altura', models.FloatField(help_text='altura del almacen')),
                ('almacen', models.ForeignKey(help_text='Almacen al que pertenece', on_delete=django.db.models.deletion.CASCADE, related_name='secciones', to='ubicacion.Almacen')),
            ],
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(help_text='codigo unico de la unidad', max_length=32, unique=True)),
                ('estado', models.BooleanField(default=True, help_text='Disponible/Usado')),
                ('producto', models.IntegerField(default=0)),
                ('fecha', models.DateField(help_text='Fecha de la ingreso')),
                ('longitud', models.FloatField(help_text='longitud de la unidad')),
                ('ancho', models.FloatField(help_text='anchura de la unidad')),
                ('altura', models.FloatField(help_text='altura de la unidad')),
                ('seccion', models.ForeignKey(help_text='Estante donde se ubicará la unidad', on_delete=django.db.models.deletion.CASCADE, related_name='unidades', to='ubicacion.Seccion')),
                ('unidad', models.ForeignKey(help_text='producto a ubicar', on_delete=django.db.models.deletion.CASCADE, related_name='unidades', to='compras.DetalleCompra')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='seccion',
            unique_together=set([('almacen', 'nombre')]),
        ),
    ]
