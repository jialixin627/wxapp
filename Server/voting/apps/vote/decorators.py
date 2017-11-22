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
            # return jsonify(common.falseReturn('', '找不到用户'))
        else:
            # if (Initiator.check_password(Users, userInfo.password, password)):
            login_time = int(decrypt['watermark']['timestamp'])
            initiator.login_time = login_time
            initiator.save()
            token = self.encode_auth_token(initiator.openid, login_time)
            return HttpResponse(json.dumps({'token': token}), content_type="application/json")
            # return jsonify(common.trueReturn(token.decode(), '登录成功'))
            # else:
            #     return jsonify(common.falseReturn('', '密码不正确'))

    def identify(self, request):
        """
        用户鉴权
        :param request
        :return: list
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            payload = self.decode_auth_token(auth_token)
            initiator = Initiator.object.filter(opneid=payload['data']['opneid']).first()
            if initiator:
                if initiator.login_time == payload['data']['login_time']:
                    openid = payload['data']['openid']
                    # return HttpResponse(json.dumps({'token': token}), content_type="application/json")
                    # result = common.trueReturn(user.id, '请求成功')
            else:
                result = common.falseReturn('', 'Token已更改，请重新登录获取')
            # else:
            #     result = common.falseReturn('', '找不到该用户信息')

auth = Auth()

def marshal(data, is_login):
    # schemas = [field() for field in fields]
    if isinstance(data, dict) and is_login:
        # return [marshal(d, fields) for d in data]
        # return HttpResponse(json.dumps({'a': 2}), content_type="application/json")
        return auth.authenticate(data)
    elif isinstance(data, str):
        return auth.identify(data)
    else:
        pass

    # type = data.get('type')
    # for schema in schemas:
    #     if type in schema.__class__.__name__.lower():
    #         result, errors = schema.dump(data)
    #         if errors:
    #             for item in errors.items():
    #                 print('{}: {}'.format(*item))
    #         return result


class marshal_with(object):
    def __init__(self, is_login):
        if not isinstance(is_login, bool):
            is_login = bool(is_login)
        self.is_login = is_login

    def __call__(self, f):
        @wraps(f)
        def wrapper(request ,*args, **kwargs):
            resp = f(request, *args, **kwargs)
            return marshal(resp, self.is_login)
        return wrapper





        # if auth_header:
        #     auth_tokenArr = auth_header.split(" ")
        #     if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
        #         result = common.falseReturn('', '请传递正确的验证头信息')
        #     else:
        #         auth_token = auth_tokenArr[1]
        #         payload = self.decode_auth_token(auth_token)
        #         if not isinstance(payload, str):
        #             user = Users.get(Users, payload['data']['id'])
        #             if (user is None):
        #                 result = common.falseReturn('', '找不到该用户信息')
        #             else:
        #                 if (user.login_time == payload['data']['login_time']):
        #                     result = common.trueReturn(user.id, '请求成功')
        #                 else:
        #                     result = common.falseReturn('', 'Token已更改，请重新登录获取')
        #         else:
        #             result = common.falseReturn('', payload)
        # else:
        #     result = common.falseReturn('', '没有提供认证token')
        # return result
