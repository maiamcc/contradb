# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0006_auto_20140820_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='dist',
            field=models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2, choices=[(0.25, 0.25), (0.5, 0.5), (0.75, 0.75), (1, 1), (1.25, 1.25), (1.5, 1.5), (1.75, 1.75), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]),
        ),
        migrations.AlterField(
            model_name='move',
            name='movename',
            field=models.CharField(max_length=100, choices=[(b'swing', b'swing'), (b'circle', b'circle'), (b'star', b'star'), (b'dosido', b'do-si-do'), (b'chain', b'chain'), (b'longlines', b'long lines'), (b'allemande', b'allemande'), (b'seesaw', b'seesaw'), (b'hey', b'hey'), (b'gypsy', b'gypsy'), (b'rlthru', b'R/L through'), (b'petronella', b'petronella'), (b'pass_ocean', b'pass the ocean'), (b'yearn', b'yearn'), (b'wave', b'wave'), (b'give_take', b'give and take'), (b'promenade', b'promenade'), (b'down_hall', b'down the hall'), (b'come_back', b'come back'), (b'other', b'other')]),
        ),
    ]
