# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0010_auto_20140904_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='bal',
            field=models.CharField(default=b'', max_length=20, null=True, blank=True, choices=[(1, True), (0, False)]),
        ),
        migrations.AlterField(
            model_name='move',
            name='hands_across',
            field=models.CharField(default=b'', max_length=20, null=True, blank=True, choices=[(1, True), (0, False)]),
        ),
        migrations.AlterField(
            model_name='move',
            name='ricochet',
            field=models.CharField(default=b'', max_length=20, null=True, blank=True, choices=[(1, True), (0, False)]),
        ),
        migrations.AlterField(
            model_name='move',
            name='rollaway',
            field=models.CharField(default=b'', max_length=20, null=True, blank=True, choices=[(1, True), (0, False)]),
        ),
    ]
