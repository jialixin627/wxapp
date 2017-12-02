# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0005_auto_20171202_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='notice_type',
            field=models.CharField(default='Notice', max_length=16, verbose_name='\u7c7b\u578b', choices=[('Notice', '\u901a\u77e5'), ('Training', '\u57f9\u8bad')]),
            preserve_default=False,
        ),
    ]
