# -*- coding: utf-8 -*-
import json
import string
import random
import requests
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from voting.apps.vote.forms import SubjectForm, ChioceFormSet, VoteForm, ChioceForm
from voting.apps.vote.models import Subject, Choice, Initiator, Participant
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .WXBizDataCrypt import WXBizDataCrypt
from django.core import serializers
from .utils import format_datetime

# Create your views here.

APPID = 'wxac49926a7c15760c'
SECRET = '80d419fdcb020d9fe4bfcfa0b70ab9c2'
initial_code = string.ascii_letters + '1234567890'
url = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'

@csrf_exempt
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
    choices = Choice.objects.filter(subject=subject).order_by('-votes')
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
def login(request):
    if request.method == "POST":
        code = request.POST.get('code', '')
        nickname = request.POST.get('nickname', '')
        avatarurl = request.POST.get('avatarUrl', '')
        status, openid, session = get_session_key(code)
        if status:
            wxapp_session = ''.join(random.sample(initial_code*2, 64))
            # cache.add(wxapp_session, openid, 2*60*60)
            initiator = Initiator.objects.filter(openid=openid)

            if initiator.exists():
                initiator = initiator.first()
                initiator.openid = openid
                initiator.wxapp_session = wxapp_session
                initiator.session = session
                initiator.nickname = nickname
                initiator.avatarurl = avatarurl
                initiator.save()
            else:
                Initiator.objects.create(openid=openid, wxapp_session=wxapp_session, session=session, nickname=nickname, avatarurl=avatarurl)

            data = json.dumps({'wxapp_session': wxapp_session, 'status': '登陆成功！'})

            return HttpResponse(data, content_type="application/json")
            # else:
            #     encryptedData = request.POST.get('encryptedData', '')
            #     iv = request.POST.get('iv', '')
            #     sessionKey = session

    #             WeUser(openid=openid, wxapp_session=wxapp_session, session=session).save()
    #         data = json.dumps({'wxapp_session': wxapp_session, 'status': '登陆成功！'})
    #         return HttpResponse(data, content_type="application/json")

    #     return HttpResponse({'status': '登陆失败！'}, content_type="application/json")
    # else:
    #     wxapp_session = request.GET.get('wxapp_session', '')
    #     return HttpResponse({'status': '登陆成功！'}, content_type="application/json")


def get_session_key(code):
    api_url = url.format(appid=APPID, secret=SECRET, code=code)
    res = requests.post(api_url).content
    data = json.loads(res)
    openid = data.get('openid', '')
    session = data.get('session_key', '')
    if openid and session:
        return True, openid, session
    else:
        return False, None, None
        #log
        #{"errcode":40029,"errmsg":"invalid code, hints: [ req_id: ok1.rA0172th40 ]"}


@csrf_exempt
def vote_list(request):
    # import time
    # time.sleep(2)
    # wxapp_session = request.POST.get('wxapp_session')
    openid = 'oKnMg0TSolZySEy1bbg9jq1ct6UU'
    # initiators = Initiator.objects.filter(wxapp_session=wxapp_session)
    # participants = Participant.objects.filter(wxapp_session=wxapp_session)
    initiators = Initiator.objects.filter(openid=openid)
    participants = Participant.objects.filter(openid=openid)
    if initiators.exists():
        initiator = initiators.first()
        i_subjects = Subject.objects.filter(initiator=initiator)
        i_data = [ s.get_subject_info() for s in i_subjects ]

    if participants.exists():
        participant = participants.first()
        choices = Choice.objects.filter(participant=participant)
        p_subjects = Subject.objects.filter(choice__in=choices)

        p_data = [ s.get_subject_info() for s in p_subjects ]

    data = {'i': i_data, 'p': p_data}
    data = json.dumps(data)

    return HttpResponse(data, content_type="application/json")

@csrf_exempt
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


@csrf_exempt
def vote_submit(request):
    pk = request.POST.get('pk', '')
    choice = Choice.objects.get(pk=pk)
    choice.votes += 1
    choice.save()
    data = json.dumps({'status': 200, 'pk': choice.subject.pk})
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def create(request):
    # import ipdb; ipdb.set_trace()
    subject_form = SubjectForm()
    choice_formset = ChioceFormSet()
    wxapp_session = request.META.get('HTTP_SESSION')
    openid = cache.get(wxapp_session)
    initiator = Initiator.objects.get(openid=openid)

    if request.method == 'POST':
        data = request.POST.dict()
        wxapp_session = data.pop('wxapp_session', '')
        deadline_date = data.pop('deadline_date', '')
        deadline_time = data.pop('deadline_time', '')
        deadline = deadline_date + ' ' + deadline_time
        data['deadline'] = deadline

        subject_form = SubjectForm(data)
        choice_formset = ChioceFormSet(data)

        if subject_form.is_valid() and choice_formset.is_valid():
            subject = subject_form.save(commit=False)
            subject.initiator = initiator
            subject.save()
            choice_formset.instance = subject
            choice_formset.save()
            return JsonResponse({'status': 200, 'pk': subject.id})
        else:
            return JsonResponse({'status': 400})
