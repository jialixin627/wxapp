# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_auto_20171115_1718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='initiator',
            old_name='session',
            new_name='session_key',
        ),
        migrations.RemoveField(
            model_name='initiator',
            name='wxapp_session',
        ),
        migrations.AddField(
            model_name='initiator',
            name='login_time',
            field=models.IntegerField(default=0),
        ),
    ]
