# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubicacion', '0002_unidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidad',
            name='producto',
            field=models.IntegerField(default=0),
        ),
    ]