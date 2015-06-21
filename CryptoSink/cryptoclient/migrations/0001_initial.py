# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='engine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_key', models.CharField(max_length=200, verbose_name=b'APP Key')),
                ('app_secret', models.CharField(max_length=200, verbose_name=b'APP Secret')),
                ('user_name', models.CharField(max_length=100, verbose_name=b'Dropbox User', blank=True)),
                ('pass_word', models.CharField(max_length=100, verbose_name=b'Dropbox Password', blank=True)),
                ('email', models.CharField(max_length=100, verbose_name=b'Dropbox Email', blank=True)),
                ('is_set', models.BooleanField(default=False, verbose_name=b'Not First Run')),
                ('public_key', models.CharField(default=b'/home/d0kt0r/Desktop/CryptoSink/CryptoSink', max_length=60, verbose_name=b'Public Key Path')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date of Creation')),
            ],
            options={
                'verbose_name': 'Dropbox Instance',
                'verbose_name_plural': 'Dropbox Instances',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='logs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_type', models.CharField(default=b'3', max_length=1, choices=[(b'0', b'File Manipulation Log'), (b'1', b'User Manipulation Log'), (b'2', b'Engine Manipulation Log'), (b'3', b'Other Errors')])),
                ('description', models.CharField(max_length=200, verbose_name=b'Description of the Log')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date of Creation')),
            ],
            options={
                'verbose_name': 'Log Instance',
                'verbose_name_plural': 'Log Instances',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='pilot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=100, verbose_name=b'File name')),
                ('timestamp', models.CharField(max_length=100, verbose_name=b'Time Stamp')),
                ('path', models.CharField(max_length=16, verbose_name=b'Path')),
                ('sym_key', models.CharField(max_length=500, verbose_name=b'Symetric Key For File')),
                ('iv', models.CharField(max_length=200, verbose_name=b'IV')),
                ('hashfile', models.CharField(max_length=600, verbose_name=b'Hash For File')),
                ('hashtime', models.CharField(max_length=600, verbose_name=b'Hash For TimeStamp')),
                ('size', models.CharField(max_length=600, verbose_name=b'File Size')),
            ],
            options={
                'verbose_name': 'File Instance',
                'verbose_name_plural': 'Files Instances',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='userapp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=50, verbose_name=b'Email', blank=True)),
                ('space_allowed', models.CharField(max_length=200, verbose_name=b'Space Allowed on dropbox', blank=True)),
                ('public_key', models.CharField(max_length=6000, verbose_name=b'User Public Key', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date of Creation')),
                ('sym_key_size', models.IntegerField(default=16, verbose_name=b'Size of the Symetric Key for encription', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pilot',
            name='user',
            field=models.ForeignKey(to='cryptoclient.userapp', blank=True),
            preserve_default=True,
        ),
    ]
