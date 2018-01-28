# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-26 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='codigo',
            field=models.CharField(help_text='codigo de la categoria', max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='codigo',
            field=models.CharField(help_text='codigo del producto', max_length=64, unique=True),
        ),
    ]