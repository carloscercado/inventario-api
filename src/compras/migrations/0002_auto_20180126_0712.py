# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-26 11:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='codigo',
            field=models.CharField(help_text='codigo de la compra', max_length=64, unique=True),
        ),
    ]
