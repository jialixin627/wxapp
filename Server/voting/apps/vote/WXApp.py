import base64
import json
from Crypto.Cipher import AES



# -*- coding: utf-8 -*-
import os
import base64
import json
import requests
from django.conf import settings
from Crypto.Cipher import AES


class WXApp(object):

    def __init__(self, code, encrypted_data, iv):
        self.js_code = code
        self.appid = settings.APPID
        self.secret = settings.SECRET
        self.encrypted_data = encrypted_data
        self.iv = iv
        self.jscode2session()

    def jscode2session(self):
        api_url = ('https://api.weixin.qq.com/sns/jscode2session?'
               'appid={}&secret={}&js_code={}&grant_type=authorization_code'
               ).format(self.appid, self.secret, self.js_code)
        resp = requests.get(api_url).json()
        self.session_key = resp.get('session_key', '')

        return resp

    def decrypt(self):
        # base64 decode
        session_key = base64.b64decode(self.session_key)
        encrypted_data = base64.b64decode(self.encrypted_data)
        iv = base64.b64decode(self.iv)

        cipher = AES.new(session_key, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encrypted_data)))

        if decrypted['watermark']['appid'] != self.appid:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
