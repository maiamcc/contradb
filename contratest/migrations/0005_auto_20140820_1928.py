# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0004_auto_20140820_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='move',
            name='beginning_info',
            field=models.CharField(default=b'', max_length=300, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='turn_how',
            field=models.CharField(default=b'', max_length=50, blank=True, choices=[(b'alone', b'alone'), (b'couple', b'as a couple')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='movename',
            field=models.CharField(max_length=100, choices=[(b'swing', b'swing'), (b'circle', b'circle'), (b'star', b'star'), (b'dosido', b'do-si-do'), (b'chain', b'chain'), (b'longlines', b'long lines'), (b'allemande', b'allemande'), (b'seesaw', b'seesaw'), (b'hey', b'hey'), (b'gypsy', b'gypsy'), (b'rlthru', b'R/L through'), (b'petronella', b'petronella'), (b'pass_ocean', b'pass the ocean'), (b'yearn', b'yearn'), (b'wave', b'wave'), (b'give_take', b'give and take'), (b'down_hall', b'down the hall'), (b'other', b'other')]),
        ),
    ]
