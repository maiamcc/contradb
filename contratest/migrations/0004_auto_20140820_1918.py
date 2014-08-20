# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0003_auto_20140820_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='move',
            name='wave_length',
            field=models.CharField(default=b'', max_length=50, blank=True, choices=[(b'short', b'short'), (b'long', b'long')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='hey_length',
            field=models.CharField(default=b'', max_length=50, blank=True, choices=[(b'half', b'half'), (b'full', b'full')]),
        ),
    ]
