#coding:utf-8
import requests
import string
import random
import json
# from django.shortcuts import render
# from django.conf import settings
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from .WXBizDataCrypt import WXBizDataCrypt
# from django.db.models import F
# from django.core.cache import cache
# from voting.apps.vote.models import Subject, Choice,
# from voting.apps.vote.forms import SubjectForm, ChioceFormSet, VoteForm, ChioceForm
# from django.core import serializers


# APPID = 'wxac49926a7c15760c'
# SECRET = '80d419fdcb020d9fe4bfcfa0b70ab9c2'
# initial_code = string.ascii_letters + '1234567890'
# url = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'


# def login(request):
#     if request.method == "POST":
#         code = request.POST.get('code', '')
#         nickname = request.POST.get('nickname', '')
#         status, openid, session = get_session_key(code)
#         if status:
#             wxapp_session = ''.join(random.sample(initial_code*2, 64))
#             cache.add(wxapp_session, openid, 2*60*60)
#             user = WeUser.objects.filter(openid=openid)

#             if user.exists():
#                 user = user.first()
#                 user.openid = openid
#                 user.wxapp_session = wxapp_session
#                 user.session = session
#                 user.nickname = nickname
#                 user.save()
#             else:
#                 WeUser.objects.create(openid=openid, wxapp_session=wxapp_session, session=session, nickname=nickname)

#             data = json.dumps({'wxapp_session': wxapp_session, 'status': '登陆成功！'})

#             return HttpResponse(data, content_type="application/json")
#             # else:
#             #     encryptedData = request.POST.get('encryptedData', '')
#             #     iv = request.POST.get('iv', '')
#             #     sessionKey = session

#     #             WeUser(openid=openid, wxapp_session=wxapp_session, session=session).save()
#     #         data = json.dumps({'wxapp_session': wxapp_session, 'status': '登陆成功！'})
#     #         return HttpResponse(data, content_type="application/json")

#     #     return HttpResponse({'status': '登陆失败！'}, content_type="application/json")
#     # else:
#     #     wxapp_session = request.GET.get('wxapp_session', '')
#     #     return HttpResponse({'status': '登陆成功！'}, content_type="application/json")


# def get_user_info(encryptedData, iv, sessionKey):
#     data = decode_user_info(encryptedData, iv, sessionKey)
#     user = WeUser.objects.filter(openid=data['openId']).first()
#     if user:
#         user.nickname = data['nickName']
#         user.save()
#     return HttpResponse(json.dumps({'status': '登陆成功！'}), content_type="application/json")



# def get_session_key(code):
#     api_url = url.format(appid=APPID, secret=SECRET, code=code)
#     res = requests.post(api_url).content
#     data = json.loads(res)
#     openid = data.get('openid', '')
#     session = data.get('session_key', '')
#     if openid and session:
#         return True, openid, session
#     else:
#         return False, None, None
#         #log
#         #{"errcode":40029,"errmsg":"invalid code, hints: [ req_id: ok1.rA0172th40 ]"}


# def decode_user_info(encryptedData, iv, sessionKey):
#     pc = WXBizDataCrypt(APPID, sessionKey)
#     user_info = pc.decrypt(encryptedData, iv)
#     return user_info





