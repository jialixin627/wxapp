# -*- coding: utf-8 -*-
import json
import random
import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from voting.apps.vote.forms import SubjectForm, ChioceFormSet, VoteForm, ChioceForm
from voting.apps.vote.models import Subject, Choice, Initiator, Participant
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .WXApp import WXApp
from django.core import serializers
from .utils import format_datetime
from .decorators import marshal_with

# Create your views here.


def index(request):
    subject_form = SubjectForm()
    choice_formset = ChioceFormSet()

    if request.method == 'POST':
        subject_form = SubjectForm(request.POST)
        choice_formset = ChioceFormSet(request.POST)

        if subject_form.is_valid() and choice_formset.is_valid():
            subject = subject_form.save()
            choice_formset.instance = subject
            choice_formset.save()
            return HttpResponseRedirect('subjects')

    return render(request, 'vote/index.html', {'subjects': subjects, 'subject_form': subject_form, 'choice_formset': choice_formset})


def subjects(request):
    subjects = Subject.objects.all().order_by('-deadline')
    return render(request, 'vote/subjects.html', {'subjects': subjects})


def voting_result(request, id):
    subject = get_object_or_404(Subject, id=id)
    choices = subject.choice_set.all().order_by('-votes')
    return render(request, 'vote/subject_result.html', {'subject': subject, 'choices': choices})


def vote_page(request, id):
    subject = get_object_or_404(Subject, id=id)
    vote_form = VoteForm(subject)
    if request.method == "POST":
        vote_form = VoteForm(subject, request.POST)
        if vote_form.is_valid():
            choice_id = vote_form.cleaned_data['choice']
            choice = Choice.objects.get(id=choice_id)
            choice.votes += 1
            choice.save()
            return HttpResponseRedirect(reverse('voting-result', args=(subject.id,)))

    return render(request, 'vote/vote_page.html', {'subject': subject, 'vote_form': vote_form})


@csrf_exempt
@marshal_with(is_login=True)
def login(request):
    if request.method == "POST":
        code = request.POST.get('code', '')
        encryptedData = request.POST.get('encryptedData', '')
        iv = request.POST.get('iv', '')
        wxapp = WXApp(code, encryptedData, iv)

        return wxapp.decrypt()

@csrf_exempt
@marshal_with(is_login=False)
def signin(request):
    return JsonResponse({'status': 200})


@csrf_exempt
@marshal_with(is_login=False)
def vote_list(request):
    initiators = Initiator.objects.filter(openid=request.openid)
    initiator = initiators.first()
    subjects = Subject.objects.filter(initiator=initiator)
    data = [ s.get_subject_info() for s in subjects ]

    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
@marshal_with(is_login=False)
def vote_list_join(request):
    participant = Participant.objects.filter(openid=request.openid).first()
    choices = Choice.objects.filter(participant=participant)
    subjects = Subject.objects.filter(choice__in=choices).distinct()
    data = [ s.get_subject_info() for s in subjects ]

    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
@marshal_with(is_login=False)
def result(request):
    pk = request.POST.get('pk', '')
    subject = Subject.objects.get(pk=pk)
    data = json.dumps(subject.to_dict())
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def get_vote_info(request):
    pk = request.POST.get('pk', '')
    subject = Subject.objects.get(pk=pk)
    data = subject.to_dict()
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")

## 没有登陆过直接进入投票页面的没考虑在内，需要增加
@csrf_exempt
@marshal_with(is_login=False)
def vote_submit(request):
    p, created = Participant.objects.update_or_create(
            openid=request.openid,
            defaults=Initiator.get_field_kv(request.openid)
        )
    pk = request.POST.get('pk', '')
    choice = Choice.objects.get(pk=pk)
    choice.votes += 1
    choice.participant_set.add(p)
    choice.save()

    data = json.dumps({'status': 200, 'pk': choice.subject.pk})
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
@marshal_with(is_login=False)
def create(request):
    subject_form = SubjectForm()
    choice_formset = ChioceFormSet()
    initiator = Initiator.objects.get(openid=request.openid)

    if request.method == 'POST':
        data = request.POST.dict()
        deadline_date = data.pop('deadline_date', '')
        deadline_time = data.pop('deadline_time', '')
        deadline = deadline_date + ' ' + deadline_time
        data['deadline'] = deadline

        subject_form = SubjectForm(data)
        choice_formset = ChioceFormSet(data)
        # import ipdb; ipdb.set_trace()

        if subject_form.is_valid() and choice_formset.is_valid():
            subject = subject_form.save(commit=False)
            subject.initiator = initiator
            subject.save()
            choice_formset.instance = subject
            choice_formset.save()
            return JsonResponse({'status': 200, 'pk': subject.id})
        else:
            return JsonResponse({'status': 400})
