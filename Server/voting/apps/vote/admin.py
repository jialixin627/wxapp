# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from voting.apps.vote.models import Subject, Choice, Initiator, Participant

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class SubjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question', 'subtitle', 'deadline', 'initiator']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'subtitle', 'pub_date', 'deadline')

admin.site.register(Initiator)
admin.site.register(Choice)
admin.site.register(Participant)
admin.site.register(Subject, SubjectAdmin)
