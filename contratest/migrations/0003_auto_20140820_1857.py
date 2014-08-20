# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0002_dance_begins'),
    ]

    operations = [
        migrations.AddField(
            model_name='move',
            name='hands_across',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='hey_length',
            field=models.CharField(default=b'', max_length=50, blank=True, choices=[(b'short', b'short'), (b'long', b'long')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='ricochet',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='rollaway',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='movename',
            field=models.CharField(max_length=100, choices=[(b'swing', b'swing'), (b'circle', b'circle'), (b'star', b'star'), (b'dosido', b'do-si-do'), (b'chain', b'chain'), (b'longlines', b'long lines'), (b'allemande', b'allemande'), (b'seesaw', b'seesaw'), (b'hey', b'hey'), (b'gypsy', b'gypsy'), (b'rlthru', b'R/L through'), (b'petronella', b'petronella'), (b'pass_ocean', b'pass the ocean'), (b'yearn', b'yearn'), (b'wave', b'wave'), (b'give_take', b'give_and_take'), (b'other', b'other')]),
        ),
    ]
