# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoclient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userapp',
            name='key_pair_size',
            field=models.IntegerField(default=1024, verbose_name=b'Size of the public/private pair', blank=True),
            preserve_default=True,
        ),
    ]
