# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_auto_20171122_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='initiator',
            name='session_key',
        ),
    ]
