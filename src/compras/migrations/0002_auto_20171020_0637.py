# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecompra',
            name='cantidad',
            field=models.FloatField(help_text='cantidad de entrada'),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='fecha',
            field=models.DateField(help_text='Fecha de la venta', null=True),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='producto',
            field=models.ForeignKey(help_text='producto', on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='productos.Producto'),
        ),
    ]
