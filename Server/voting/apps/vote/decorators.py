# coding:utf8
import jwt
import json
import datetime
from functools import wraps
from django.conf import settings
from voting.apps.vote.models import WeUser
from django.http import HttpResponse
from django.utils.decorators import available_attrs


class Auth():
    @staticmethod
    def encode_auth_token(openid, timestamp):
        """
        生成认证Token
        :param openid: str
        :param timestamp: int
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10), # noqa
                'iat': datetime.datetime.utcnow(),
                'iss': 'jialixin',
                'data': {
                    'openid': openid,
                    'timestamp': timestamp
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
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'),
            #                       leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, settings.SECRET_KEY,
                                 options={'verify_exp': False})
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
        weuser = WeUser.objects.filter(openid=openid).first()

        if weuser:
            timestamp = int(decrypt['watermark']['timestamp'])
            weuser.timestamp = timestamp
            weuser.nickname = decrypt.get('nickName')
            weuser.save()
            token = self.encode_auth_token(weuser.openid, timestamp)
            return HttpResponse(
                    json.dumps(
                        {'token': token}), content_type="application/json")
        else:
            weuser = WeUser.objects.create(
                openid=openid,
                nickname=decrypt.get('nickName'),
                avatarurl=decrypt.get('avatarUrl'),
                timestamp=decrypt['watermark']['timestamp']
            )
            token = self.encode_auth_token(weuser.openid,
                                           weuser.timestamp)
            return HttpResponse(
                    json.dumps({'token': token}),
                    content_type="application/json")

    def identify(self, request):
        """
        用户鉴权
        :param request
        :return: json or None
        """
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        if auth_token:
            payload = self.decode_auth_token(auth_token)
            openid = payload['data']['openid']
            weuser = WeUser.objects.filter(openid=openid).first()
            if weuser:
                if weuser.timestamp == payload['data']['timestamp']:
                        request.openid = openid
                        return
                else:
                    return json.dumps(
                        {'status': 'Token已更改，请重新登录获取', 'resNo': 400})
            else:
                return json.dumps({'status': '验证不通过，请重新登录获取', 'resNo': 400})
        else:
            return json.dumps({'status': '没有提供Token，请重新登录获取', 'resNo': 400})


auth = Auth()


class authentication(object):
    def __init__(self, is_login):
        if not isinstance(is_login, bool):
            is_login = bool(is_login)
        self.is_login = is_login

    def __call__(self, f):
        @wraps(f, assigned=available_attrs(f))
        def wrapper(request, *args, **kwargs):
            if self.is_login:
                resp = f(request, *args, **kwargs)
                return auth.authenticate(resp)
            else:
                result = auth.identify(request)
                if result:
                    return HttpResponse(result, content_type="application/json") # noqa
            return f(request, *args, **kwargs)
        return wrapper
