# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 15:50
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0003_auto_20171022_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallecompra',
            name='precio',
            field=models.DecimalField(decimal_places=8, default=Decimal('0'), help_text='Precio unitario del producto', max_digits=16),
        ),
    ]