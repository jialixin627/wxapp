# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from voting.apps.vote.models import WeUser, Notice, Questionnaire, \
     Question, QuestionOption, Answer, Attendance

# Register your models here.

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class QuestionnaireAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'tagline', 'deadline', 'weuser']}),
    ]
    inlines = [QuestionInline]
    list_display = ('title', 'pubdate', 'deadline', 'weuser')


class WeUserAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['nickname', 'rename', 'date_created']}),
    # ]
    list_display = ('nickname', 'rename', 'date_created')

# class QuestionAdmin(admin.ModelAdmin):
#     pass

admin.site.register(WeUser, WeUserAdmin)
admin.site.register(Notice)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(Answer)
admin.site.register(Attendance)
