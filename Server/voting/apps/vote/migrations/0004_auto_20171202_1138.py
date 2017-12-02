# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_auto_20171202_1130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weuser',
            options={'ordering': ['-date_created'], 'verbose_name': '\u5458\u5de5\u4fe1\u606f', 'verbose_name_plural': '\u5458\u5de5\u4fe1\u606f'},
        ),
        migrations.AlterField(
            model_name='weuser',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
    ]
