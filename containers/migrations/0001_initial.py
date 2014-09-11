# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Containers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CId', models.CharField(max_length=30)),
                ('Name', models.CharField(max_length=30)),
                ('Owner', models.CharField(max_length=30)),
                ('PortMap', models.CharField(max_length=30)),
                ('Created', models.CharField(max_length=30)),
                ('Living', models.CharField(max_length=30)),
                ('Status', models.CharField(max_length=30)),
                ('Project', models.CharField(max_length=30)),
                ('CodeVersion', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
