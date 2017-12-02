# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_auto_20171202_1138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': '\u7b54\u6848', 'verbose_name_plural': '\u7b54\u6848'},
        ),
        migrations.AlterModelOptions(
            name='notice',
            options={'ordering': ['-date_created'], 'verbose_name': '\u6d3b\u52a8-\u901a\u77e5', 'verbose_name_plural': '\u6d3b\u52a8-\u901a\u77e5'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': '\u95ee\u9898', 'verbose_name_plural': '\u95ee\u9898'},
        ),
        migrations.AlterModelOptions(
            name='questionnaire',
            options={'ordering': ['-pubdate'], 'verbose_name': '\u95ee\u5377\u8c03\u67e5', 'verbose_name_plural': '\u95ee\u5377\u8c03\u67e5'},
        ),
        migrations.AlterModelOptions(
            name='questionoption',
            options={'verbose_name': '\u9009\u9879', 'verbose_name_plural': '\u9009\u9879'},
        ),
    ]
