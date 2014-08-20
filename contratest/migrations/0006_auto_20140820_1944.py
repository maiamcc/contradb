# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0005_auto_20140820_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='movename',
            field=models.CharField(max_length=100, choices=[(b'swing', b'swing'), (b'circle', b'circle'), (b'star', b'star'), (b'dosido', b'do-si-do'), (b'chain', b'chain'), (b'longlines', b'long lines'), (b'allemande', b'allemande'), (b'seesaw', b'seesaw'), (b'hey', b'hey'), (b'gypsy', b'gypsy'), (b'rlthru', b'R/L through'), (b'petronella', b'petronella'), (b'pass_ocean', b'pass the ocean'), (b'yearn', b'yearn'), (b'wave', b'wave'), (b'give_take', b'give and take'), (b'promenade', b'promenade'), (b'down_hall', b'down the hall'), (b'other', b'other')]),
        ),
    ]
