# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0015_auto_20141106_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='move',
            name='rollaway',
        ),
    ]
