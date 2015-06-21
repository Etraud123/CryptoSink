# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoclient', '0002_userapp_key_pair_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pilot',
            name='user',
            field=models.ForeignKey(to='cryptoclient.userapp'),
            preserve_default=True,
        ),
    ]
