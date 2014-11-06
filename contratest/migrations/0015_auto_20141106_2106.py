# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratest', '0014_auto_20141106_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='move',
            name='wave_type',
        ),
        migrations.AddField(
            model_name='move',
            name='bal_dir',
            field=models.CharField(default=b'', max_length=50, blank=True, choices=[(b'RL', b'right, then left'), (b'LR', b'left, then right'), (b'fwd_back', b'forward and back')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='move',
            name='progress',
            field=models.CharField(default=b'', max_length=50, blank=True, choices=[(b'pass_thru', b'pass through'), (b'slide_left', b'slide left'), (b'slide_right', b'slide right')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='move',
            name='dir',
            field=models.CharField(default=b'', max_length=20, blank=True, choices=[(b'L', b'left'), (b'R', b'right'), (b'across', b'across'), (b'ldiag', b'left diagonal'), (b'rdiag', b'right diagonal'), (b'sides', b'on the sides')]),
        ),
        migrations.AlterField(
            model_name='move',
            name='movename',
            field=models.CharField(max_length=100, choices=[(b'swing', b'swing'), (b'circle', b'circle'), (b'star', b'star'), (b'dosido', b'do-si-do'), (b'chain', b'chain'), (b'longlines', b'long lines'), (b'allemande', b'allemande'), (b'seesaw', b'seesaw'), (b'hey', b'hey'), (b'gypsy', b'gypsy'), (b'rlthru', b'R/L through'), (b'petronella', b'petronella'), (b'pass_ocean', b'pass the ocean'), (b'yearn', b'yearn'), (b'bal_wave', b'balance the wave'), (b'give_take', b'give and take'), (b'promenade', b'promenade'), (b'down_hall', b'down the hall'), (b'come_back', b'come back'), (b'mad_robin', b'mad robin'), (b'other', b'other')]),
        ),
    ]
