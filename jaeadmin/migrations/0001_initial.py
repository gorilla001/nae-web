# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DockerFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=30)),
                ('Size', models.IntegerField()),
                ('Created', models.DateTimeField()),
                ('CreatedBy', models.CharField(max_length=30)),
                ('Modified', models.DateTimeField()),
                ('ModifiedBy', models.CharField(max_length=30)),
                ('Path', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ProjectID', models.CharField(max_length=10)),
                ('Name', models.CharField(max_length=30)),
                ('Description', models.CharField(max_length=200)),
                ('Image', models.CharField(max_length=30)),
                ('Admin', models.CharField(max_length=30)),
                ('Member', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
