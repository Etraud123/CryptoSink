# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoclient', '0003_auto_20150203_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='user',
            field=models.ForeignKey(to='cryptoclient.userapp', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pilot',
            name='size',
            field=models.IntegerField(default=0, verbose_name=b'Size of the file'),
            preserve_default=True,
        ),
    ]
