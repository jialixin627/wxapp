#coding:utf8
import jwt, datetime, time
# from app.users.model import Users
from functools import wraps
from django.utils import timezone
from django.conf import settings
from .models import Initiator, Participant
import json
from django.http import HttpResponse


class Auth():
    @staticmethod
    def encode_auth_token(openid, login_time):
        """
        生成认证Token
        :param openid: str
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'jialixin',
                'data': {
                    'openid': openid,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                settings.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, settings.SECRET_KEY, options={'verify_exp': False})
            if ('data' in payload and 'openid' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'


    def authenticate(self, decrypt):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param decrypt:
        :return: json
        """
        openid = decrypt.get('openId', '')
        initiator = Initiator.objects.filter(openid=openid).first()

        if not initiator:
            Initiator.objects.create(
                openid=openid,
                nickname=decrypt.get('nickName'),
                avatarurl=decrypt.get('avatarUrl'),
                login_time=decrypt['watermark']['timestamp']
            )
            token = self.encode_auth_token(initiator.openid, initiator.login_time)
            return HttpResponse(json.dumps({'token': token}), content_type="application/json")
        else:
            login_time = int(decrypt['watermark']['timestamp'])
            initiator.login_time = login_time
            initiator.save()
            token = self.encode_auth_token(initiator.openid, login_time)
            return HttpResponse(json.dumps({'token': token}), content_type="application/json")

    def identify(self, request):
        """
        用户鉴权
        :param request
        :return: json or None
        """
        auth_token = request.META.get('HTTP_AUTHORIZATION').split(" ")[-1]
        if auth_token:
            payload = self.decode_auth_token(auth_token)
            openid = payload['data']['openid']
            initiator = Initiator.objects.filter(openid=openid).first()
            if initiator:
                if initiator.login_time == payload['data']['login_time']:
                        request.openid = openid
                        return
                else:
                    return json.dumps({'status': 'Token已更改，请重新登录获取', 'resNo': 400 })
            else:
                return json.dumps({'status': '验证不通过，请重新登录获取', 'resNo': 400 })


auth = Auth()

# def marshal(data, is_login):
#     if isinstance(data, dict) and is_login:
#         return auth.authenticate(data)
#     elif isinstance(data, str):
#         return auth.identify(data)


class marshal_with(object):
    def __init__(self, is_login):
        if not isinstance(is_login, bool):
            is_login = bool(is_login)
        self.is_login = is_login

    def __call__(self, f):
        @wraps(f)
        def wrapper(request ,*args, **kwargs):
            # resp = f(request, *args, **kwargs)
            # return marshal(resp, self.is_login)
            if self.is_login:
                resp = f(request, *args, **kwargs)
                return auth.authenticate(resp)
            else:
                result = auth.identify(request)
                if result:
                    return HttpResponse(result, content_type="application/json")
                return f(request, *args, **kwargs)
        return wrapper
