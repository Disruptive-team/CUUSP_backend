import datetime
import os

import jwt
from .builtin_code_util import RespStatus


class FlaskJWT():
    def __init__(self, app=None):
        self._app = app
        self._secret_key = None

    def init_app(self, app):
        if self._app is None:
            self._app = app
        if "JWT_SECRET_KEY" in app.config:
            self._secret_key = app.config.get("JWT_SECRET_KEY")
        elif "JWT_SECRET_KEY" in os.environ:
            self._secret_key = os.environ.get("JWT_SECRET_KEY")
        else:
            raise ValueError('Missing required configuration data for '
                             'JWT_SECRET_KEY.')

    def encode_auth_token(self, data: dict):
        # 申请Token,参数为自定义,user_id不必须,此处为以后认证作准备,程序员可以根据情况自定义不同参数
        """
        生成认证Token
        :param data: dict
        :param login_time: int(timestamp)
        :return: string
        """
        try:

            headers = {
                "typ": "JWT",
                "alg": "HS256",
            }

            playload = {
                "headers": headers,
                "iss": 'K.Deng',
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=99, hours=0, minutes=0, seconds=0),
                'iat': datetime.datetime.utcnow(),
                "data": data
            }

            signature = jwt.encode(playload, self._secret_key, algorithm='HS256')
            return signature

        except Exception as e:
            return e

        # encode为加密函数，decode为解密函数(HS256)

        # JWT官网的三个加密参数为
        # 1.header(type,algorithm)
        #  {
        #  "alg": "HS256",
        #  "typ": "JWT"
        #  }
        # 2.playload(iss,sub,aud,exp,nbf,lat,jti)
        #   iss: jwt签发者
        #   sub: jwt所面向的用户
        #   aud: 接收jwt的一方
        #   exp: jwt的过期时间，这个过期时间必须要大于签发时间
        #   nbf: 定义在什么时间之前，该jwt都是不可用的.
        #   iat: jwt的签发时间
        #   jti: jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。
        # 3.signature
        #
        # jwt的第三部分是一个签证信息，这个签证信息由三部分组成：
        #
        #    header (base64后的)
        #    payload (base64后的)
        #    secret

        # PyJwt官网的三个加密参数为
        # jwt.encode(playload, key, algorithm='HS256')
        # playload 同上,key为app的 SECRET_KEY algorithm 为加密算法

        # 二者应该都可以用，但我们用的是python的 pyjwt ，那就入乡随俗吧

    def decode_auth_token(self, auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, self._secret_key, options={'verify_exp': False}, algorithms='HS256')
            if payload:
                return payload
            else:
                raise jwt.InvalidTokenError

        except jwt.ExpiredSignatureError:
            return RespStatus.ExpiredSignature

        except jwt.InvalidTokenError:
            return RespStatus.InvalidToken
