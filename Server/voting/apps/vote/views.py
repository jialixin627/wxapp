# -*- coding: utf-8 -*-
import json
from .WXApp import WXApp
from .decorators import authentication

from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

# from voting.apps.vote.forms import SubjectForm, ChioceFormSet, VoteForm
from voting.apps.vote.models import WeUser, Notice, Questionnaire, \
     Question, QuestionOption, Answer, Attendance


# @csrf_exempt
@authentication(is_login=True)
def login(request):
    if request.method == "POST":
        code = request.POST.get('code', '')
        encryptedData = request.POST.get('encryptedData', '')
        iv = request.POST.get('iv', '')
        wxapp = WXApp(code, encryptedData, iv)

        return wxapp.decrypt()


# @csrf_exempt
@authentication(is_login=False)
def signin(request):
    return JsonResponse({'status': 200})


# @csrf_exempt
@authentication(is_login=False)
def notice_list(request):
    weuser = WeUser.objects.get(openid=request.openid)
    notice_list = Notice.objects.filter(attendance__weuser=weuser)
    print notice_list.values_list(flat=True)
    # data = [s.get_subject_info() for s in subjects]
    data = {}

    return HttpResponse(json.dumps(data), content_type="application/json")


# def index(request):
#     subject_form = SubjectForm()
#     choice_formset = ChioceFormSet()

#     if request.method == 'POST':
#         subject_form = SubjectForm(request.POST)
#         choice_formset = ChioceFormSet(request.POST)

#         if subject_form.is_valid() and choice_formset.is_valid():
#             subject = subject_form.save()
#             choice_formset.instance = subject
#             choice_formset.save()
#             return HttpResponseRedirect('subjects')
#     data = {
#         'subjects': subjects,
#         'subject_form': subject_form,
#         'choice_formset': choice_formset
#     }

#     return render(request, 'vote/index.html', data)


# def subjects(request):
#     subjects = Subject.objects.all().order_by('-deadline')
#     return render(request, 'vote/subjects.html', {'subjects': subjects})


# def voting_result(request, id):
#     subject = get_object_or_404(Subject, id=id)
#     choices = subject.choice_set.all().order_by('-votes')
#     return render(request, 'vote/subject_result.html', {'subject': subject,
#                                                         'choices': choices})


# def vote_page(request, id):
#     subject = get_object_or_404(Subject, id=id)
#     vote_form = VoteForm(subject)
#     if request.method == "POST":
#         vote_form = VoteForm(subject, request.POST)
#         if vote_form.is_valid():
#             choice_id = vote_form.cleaned_data['choice']
#             choice = Choice.objects.get(id=choice_id)
#             choice.votes += 1
#             choice.save()
#             return HttpResponseRedirect(
#                     reverse('voting-result', args=(subject.id,)))

#     return render(request, 'vote/vote_page.html', {'subject': subject,
#                                                    'vote_form': vote_form})


# @csrf_exempt
# @authentication(is_login=False)
# def vote_list_join(request):
#     participant = Participant.objects.filter(openid=request.openid).first()
#     choices = Choice.objects.filter(participant=participant)
#     subjects = Subject.objects.filter(choice__in=choices).distinct()
#     data = [s.get_subject_info() for s in subjects]

#     return HttpResponse(json.dumps(data), content_type="application/json")


# @csrf_exempt
# @authentication(is_login=False)
# def get_vote_info(request):
#     pk = request.POST.get('pk', '')
#     subject = Subject.objects.get(pk=pk)
#     participant = Participant.objects.filter(openid=request.openid)
#     initiator = Initiator.objects.get(openid=request.openid)
#     voted = subject.choice_set.all().filter(
#                 participant__in=participant).exists()
#     is_initiator = initiator == subject.initiator
#     data = subject.to_dict()
#     data.update({'voted': voted, 'is_initiator': is_initiator})
#     return HttpResponse(json.dumps(data), content_type="application/json")


# @csrf_exempt
# @authentication(is_login=False)
# def vote_submit(request):
#     p, created = Participant.objects.update_or_create(
#             openid=request.openid,
#             defaults=Initiator.get_field_kv(request.openid)
#         )
#     pk = request.POST.get('pk', '')
#     choice = Choice.objects.get(pk=pk)
#     choice.votes += 1
#     choice.participant_set.add(p)
#     choice.save()

#     data = json.dumps({'status': 200, 'pk': choice.subject.pk})
#     return HttpResponse(data, content_type="application/json")


# @csrf_exempt
# @authentication(is_login=False)
# def create(request):
#     subject_form = SubjectForm()
#     choice_formset = ChioceFormSet()
#     initiator = Initiator.objects.get(openid=request.openid)

#     if request.method == 'POST':
#         data = request.POST.dict()
#         deadline_date = data.pop('deadline_date', '')
#         deadline_time = data.pop('deadline_time', '')
#         deadline = deadline_date + ' ' + deadline_time
#         data['deadline'] = deadline

#         subject_form = SubjectForm(data)
#         choice_formset = ChioceFormSet(data)

#         if subject_form.is_valid() and choice_formset.is_valid():
#             subject = subject_form.save(commit=False)
#             subject.initiator = initiator
#             subject.save()
#             choice_formset.instance = subject
#             choice_formset.save()
#             return JsonResponse({'status': 200, 'pk': subject.id})
#         else:
#             return JsonResponse({'status': 400})

