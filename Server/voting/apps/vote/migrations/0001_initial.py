# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice_text', models.CharField(max_length=256)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Initiator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(unique=True, max_length=128)),
                ('session', models.CharField(unique=True, max_length=255)),
                ('wxapp_session', models.CharField(unique=True, max_length=255)),
                ('nickname', models.CharField(default='', max_length=56)),
                ('avatarurl', models.CharField(default='', max_length=128)),
                ('rename', models.CharField(default='', max_length=56, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(unique=True, max_length=128)),
                ('session', models.CharField(unique=True, max_length=255)),
                ('wxapp_session', models.CharField(unique=True, max_length=255)),
                ('nickname', models.CharField(default='', max_length=56)),
                ('avatarurl', models.CharField(default='', max_length=128)),
                ('rename', models.CharField(default='', max_length=56, null=True, blank=True)),
                ('choice', models.ForeignKey(to='vote.Choice')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=255, verbose_name='\u6295\u7968\u6807\u9898')),
                ('subtitle', models.CharField(max_length=255, null=True, verbose_name='\u5185\u5bb9\u8865\u5145', blank=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('deadline', models.DateTimeField(verbose_name='\u622a\u6b62\u65e5\u671f')),
                ('initiator', models.ForeignKey(to='vote.Initiator')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='subject',
            field=models.ForeignKey(to='vote.Subject'),
        ),
    ]
