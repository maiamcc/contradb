# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0008_auto_20140904_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='bal',
            field=models.CharField(default=b'', max_length=20, blank=True, choices=[(1, b'True'), (0, b'False')]),
        ),
        migrations.AlterField(
            model_name='move',
            name='hands_across',
            field=models.CharField(default=b'', max_length=20, blank=True, choices=[(1, b'True'), (0, b'False')]),
        ),
        migrations.AlterField(
            model_name='move',
            name='ricochet',
            field=models.CharField(default=b'', max_length=20, blank=True, choices=[(1, b'True'), (0, b'False')]),
        ),
        migrations.AlterField(
            model_name='move',
            name='rollaway',
            field=models.CharField(default=b'', max_length=20, blank=True, choices=[(1, b'True'), (0, b'False')]),
        ),
    ]
