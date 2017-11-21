# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='choice',
        ),
        migrations.AddField(
            model_name='participant',
            name='choice',
            field=models.ManyToManyField(to='vote.Choice'),
        ),
    ]
