# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_text', models.TextField(null=True, verbose_name='\u6587\u5b57\u7b54\u6848', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sign_in_time', models.DateTimeField(auto_now=True, verbose_name='\u67e5\u770b\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u901a\u77e5\u67e5\u770b',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60, verbose_name='\u901a\u77e5\u6807\u9898')),
                ('content', models.CharField(max_length=60, verbose_name='\u901a\u77e5\u5185\u5bb9')),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_type', models.PositiveSmallIntegerField(default=1, verbose_name='\u95ee\u9898\u7c7b\u578b', choices=[(1, '\u6587\u5b57'), (2, '\u5355\u9009'), (3, '\u591a\u9009')])),
                ('subject', models.CharField(max_length=1024, verbose_name='\u95ee\u9898')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='\u95ee\u5377\u6807\u9898')),
                ('tagline', models.TextField(null=True, verbose_name='\u5185\u5bb9\u8865\u5145', blank=True)),
                ('pubdate', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('deadline', models.DateTimeField(null=True, verbose_name='\u622a\u6b62\u65e5\u671f', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option', models.CharField(max_length=256, verbose_name='\u9009\u9879')),
                ('question', models.ForeignKey(verbose_name='\u95ee\u9898', to='vote.Question')),
            ],
        ),
        migrations.CreateModel(
            name='WeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(unique=True, max_length=128)),
                ('nickname', models.CharField(default='', max_length=56, verbose_name='\u6635\u79f0')),
                ('avatarurl', models.CharField(default='', max_length=128, verbose_name='\u5934\u50cf')),
                ('timestamp', models.IntegerField(default=0)),
                ('rename', models.CharField(default='', max_length=56, null=True, verbose_name='\u59d3\u540d', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='weuser',
            field=models.ForeignKey(verbose_name='\u95ee\u5377\u7f16\u8f91\u4eba', to='vote.WeUser'),
        ),
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(verbose_name='\u95ee\u5377\u6807\u9898', to='vote.Questionnaire'),
        ),
        migrations.AddField(
            model_name='notice',
            name='weuser',
            field=models.ForeignKey(verbose_name='\u53d1\u8d77\u4eba', to='vote.WeUser'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='notice',
            field=models.ForeignKey(to='vote.Notice'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='weuser',
            field=models.ForeignKey(to='vote.WeUser'),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_option',
            field=models.ForeignKey(verbose_name='\u9009\u9879\u7b54\u6848', blank=True, to='vote.QuestionOption', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(verbose_name='\u95ee\u9898', to='vote.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='weuser',
            field=models.ForeignKey(verbose_name='\u7b54\u9898\u8005', to='vote.WeUser'),
        ),
    ]
