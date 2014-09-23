# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0012_auto_20140904_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='dist',
            field=models.CharField(default=b'', max_length=20, blank=True, choices=[(0.25, 0.25), (0.5, 0.5), (0.75, 0.75), (1, 1), (1.25, 1.25), (1.5, 1.5), (1.75, 1.75), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]),
        ),
    ]
