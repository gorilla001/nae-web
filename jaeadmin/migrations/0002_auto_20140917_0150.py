# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jaeadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockerfiles',
            name='Created',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='dockerfiles',
            name='Modified',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='dockerfiles',
            name='Size',
            field=models.CharField(max_length=30),
        ),
    ]
