# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_remove_initiator_session_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='session',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='wxapp_session',
        ),
    ]
