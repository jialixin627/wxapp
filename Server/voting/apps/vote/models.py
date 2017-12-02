# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .utils import format_datetime


class WeUser(models.Model):
    openid = models.CharField(max_length=128, unique=True)
    nickname = models.CharField(u'昵称', max_length=56, default='')
    avatarurl = models.CharField(u'头像', max_length=128, default='')
    timestamp = models.IntegerField(default=0)
    rename = models.CharField(u'姓名', max_length=56, default='', blank=True, null=True)
    date_created = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = u'员工信息'
        ordering = ['-date_created']

    def __unicode__(self):
        return self.rename or self.nickname

    @classmethod
    def get_field_kv(cls, openid):
        s = cls.objects.get(openid=openid)
        data = {
            'openid': s.openid,
            'nickname': s.nickname,
            'avatarurl': s.avatarurl,
            'rename': s.rename
        }
        return data


class Notice(models.Model):
    TYPE_CHOICES = (
        ('Notice', '通知'),
        ('Training', '培训')
    )
    title = models.CharField(u'通知标题', max_length=60)
    content = models.TextField(u'通知内容')
    notice_type = models.CharField(u'类型', max_length=16, choices=TYPE_CHOICES)
    date_created = models.DateTimeField(auto_now=True)
    weuser = models.ForeignKey(WeUser, verbose_name=u'发起人')

    class Meta:
        verbose_name = verbose_name_plural = u'活动-通知'
        ordering = ['-date_created']

    def __unicode__(self):
        return self.title


class Questionnaire(models.Model):
    title = models.CharField(u'问卷标题', max_length=128)
    tagline = models.TextField(u'内容补充', blank=True, null=True)
    pubdate = models.DateTimeField(u'发布时间', auto_now_add=True)
    deadline = models.DateTimeField(u'截止日期', blank=True, null=True)
    weuser = models.ForeignKey(WeUser, verbose_name=u'问卷编辑人')

    class Meta:
        verbose_name = verbose_name_plural = u'问卷调查'
        ordering = ['-pubdate']

    def __unicode__(self):
        return self.title

    # def total_votes(self):
    #     return sum(self.choice_set.all().values_list('votes', flat=True))

    # def get_subject_info(self):
    #     data = {
    #         'pk': self.pk,
    #         'name': self.initiator.rename or self.initiator.nickname,
    #         'avatarurl': self.initiator.avatarurl,
    #         'question': self.question,
    #         'subtitle': self.subtitle,
    #         'deadline': format_datetime(self.deadline),
    #         'total_votes': self.total_votes(),
    #     }
    #     return data

    # def get_all_chioces(self):
    #     choices = self.choice_set.all()
    #     choice_list = [
    #         {
    #             'pk': choice.pk,
    #             'subject_pk': self.pk,
    #             'votes': choice.votes,
    #             'choice_text': choice.choice_text,
    #             'proportion': '{:.2f}'.format(float(choice.votes*100)/self.total_votes()) \
    #                                                                 if choice.votes else 0
    #         }
    #         for choice in choices
    #     ]
    #     return choice_list

    # def to_dict(self):
    #     data = self.get_subject_info()
    #     data.update({
    #         'choices_data': self.get_all_chioces()
    #     })
    #     return data


class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        (1, u'文字'),
        (2, u'单选'),
        (3, u'多选'),
    )
    question_type = models.PositiveSmallIntegerField(u'问题类型',
                        choices=QUESTION_TYPE_CHOICES, default=1)
    subject = models.CharField(u'问题', max_length=1024)
    questionnaire = models.ForeignKey(Questionnaire, verbose_name=u'问卷标题')

    class Meta:
        verbose_name = verbose_name_plural = u'问题'

    def __unicode__(self):
        return self.subject



class QuestionOption(models.Model):
    question = models.ForeignKey(Question, verbose_name=u'问题')
    option = models.CharField(u'选项', max_length=256)

    class Meta:
        verbose_name = verbose_name_plural = u'选项'

    def __unicode__(self):
        return self.option


class Answer(models.Model):
    weuser = models.ForeignKey(WeUser, verbose_name=u'答题者')
    question = models.ForeignKey(Question, verbose_name=u'问题')
    answer_text = models.TextField(u'文字答案', blank=True, null=True)
    answer_option = models.ForeignKey(QuestionOption,
                        verbose_name=u'选项答案', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = u'答案'


class Attendance(models.Model):
    notice = models.ForeignKey(Notice)
    weuser = models.ForeignKey(WeUser)
    sign_in_time = models.DateTimeField(u'查看时间', auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = u'通知查看'
        unique_together = ('notice', 'weuser')
        index_together = ['notice', 'weuser']

    def __unicode__(self):
        return '%s - %s' % (self.notice.title,
                self.weuser.nickname or self.weuser.rename)

