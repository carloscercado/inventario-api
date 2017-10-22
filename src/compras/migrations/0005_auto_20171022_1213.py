# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0004_auto_20171022_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='procesada',
            field=models.BooleanField(default=False, help_text='Estatus del procesamiento de la compra'),
        ),
        migrations.AlterField(
            model_name='detallecompra',
            name='precio',
            field=models.DecimalField(decimal_places=8, help_text='Precio unitario del producto', max_digits=16),
        ),
    ]
