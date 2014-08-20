# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('formation', models.CharField(default=b'improper', max_length=200)),
                ('progression', models.IntegerField(default=1)),
                ('tags', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seq', models.IntegerField(null=True)),
                ('sect', models.CharField(max_length=2, null=True, choices=[(b'A1', b'A1'), (b'A2', b'A2'), (b'B1', b'B1'), (b'B2', b'B2')])),
                ('movename', models.CharField(max_length=100, choices=[(b'swing', b'swing'), (b'circle', b'circle'), (b'star', b'star'), (b'dosido', b'do-si-do'), (b'chain', b'chain'), (b'longlines', b'long lines'), (b'allemande', b'allemande')])),
                ('who', models.CharField(default=b'', max_length=20, blank=True, choices=[(b'ladies', b'ladies'), (b'gents', b'gents'), (b'partner', b'partner'), (b'neighbor', b'neighbor'), (b'shadow', b'shadow')])),
                ('hand', models.CharField(default=b'', max_length=20, blank=True, choices=[(b'L', b'left'), (b'R', b'right')])),
                ('dist', models.DecimalField(null=True, max_digits=3, decimal_places=2, blank=True)),
                ('dir', models.CharField(default=b'', max_length=20, blank=True, choices=[(b'L', b'left'), (b'R', b'right'), (b'across', b'across'), (b'ldiag', b'left diagonal'), (b'rdiag', b'right diagonal')])),
                ('bal', models.NullBooleanField()),
                ('count', models.IntegerField(default=8, null=True)),
                ('moreinfo', models.CharField(default=b'', max_length=300, blank=True)),
                ('dance', models.ForeignKey(to='contratest.Dance')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
