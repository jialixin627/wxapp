# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_auto_20171202_1122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'verbose_name': '\u901a\u77e5\u67e5\u770b', 'verbose_name_plural': '\u901a\u77e5\u67e5\u770b'},
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set([('notice', 'weuser')]),
        ),
        migrations.AlterIndexTogether(
            name='attendance',
            index_together=set([('notice', 'weuser')]),
        ),
    ]
