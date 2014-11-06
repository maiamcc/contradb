# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0013_auto_20140922_2015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='move',
            name='wave_length',
        ),
        migrations.AddField(
            model_name='move',
            name='wave_type',
            field=models.CharField(default=b'', max_length=50, blank=True, choices=[(b'short', b'short'), (b'long', b'long'), (b'ladies', b'ladies'), (b'gents', b'gents')]),
            preserve_default=True,
        ),
    ]
