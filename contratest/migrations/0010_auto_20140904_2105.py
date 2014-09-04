# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0009_auto_20140904_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='bal',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(1, True), (0, False)]),
        ),
        migrations.AlterField(
            model_name='move',
            name='hands_across',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(1, True), (0, False)]),
        ),
        migrations.AlterField(
            model_name='move',
            name='ricochet',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(1, True), (0, False)]),
        ),
        migrations.AlterField(
            model_name='move',
            name='rollaway',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(1, True), (0, False)]),
        ),
    ]
