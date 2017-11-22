# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .utils import format_datetime

# Create your models here.


class Initiator(models.Model):
    openid = models.CharField(max_length=128, unique=True)
    # session_key = models.CharField(max_length=255, unique=True)
    # wxapp_session = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=56, default='')
    avatarurl = models.CharField(max_length=128, default='')
    login_time = models.IntegerField(default=0)
    rename = models.CharField(max_length=56, default='', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.rename or self.nickname


class Subject(models.Model):
    question = models.CharField('投票标题', max_length=255)
    subtitle = models.CharField('内容补充', max_length=255, blank=True, null=True)
    pub_date = models.DateTimeField('发布时间', auto_now_add=True)
    deadline = models.DateTimeField('截止日期')
    initiator = models.ForeignKey(Initiator)

    def __unicode__(self):
        return self.question

    def total_votes(self):
        return sum(self.choice_set.all().values_list('votes', flat=True))

    def get_subject_info(self):
        data = {
            'pk': self.pk,
            'name': self.initiator.rename or self.initiator.nickname,
            'avatarurl': self.initiator.avatarurl,
            'question': self.question,
            'subtitle': self.subtitle,
            'deadline': format_datetime(self.deadline),
            'total_votes': self.total_votes(),
        }
        return data

    def get_all_chioces(self):
        choices = self.choice_set.all()
        choice_list = [
            {
                'votes': choice.votes,
                'choice_text': choice.choice_text,
                'pk': choice.pk,
                'subject_pk': self.pk,
                'proportion': '{:.2f}'.format(float(choice.votes*100)/self.total_votes()) if choice.votes else 0
            }
            for choice in choices
        ]
        return choice_list

    def to_dict(self):
        data = self.get_subject_info()
        data.update({
            'choices_data': self.get_all_chioces()
        })
        return data


class Choice(models.Model):
    subject = models.ForeignKey(Subject)
    choice_text = models.CharField(max_length=256)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text

    # def to_dict(self):
    #     return


class Participant(models.Model):
    openid = models.CharField(max_length=128, unique=True)
    session = models.CharField(max_length=255, unique=True)
    wxapp_session = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=56, default='')
    avatarurl = models.CharField(max_length=128, default='')
    rename = models.CharField(max_length=56, default='', blank=True, null=True)
    choice = models.ManyToManyField(Choice)

    def __unicode__(self):
        return self.rename or self.nickname
