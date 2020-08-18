#!/usr/bin/env python
# -*- coding:utf-8 -*-
import jwt
import datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

JWT_SALT = 'iv%x6xo7l7_u9bf_u!9#g#m*)*=ej@bek5)(@u3kh*72+unjv='


def create_token(payload, timeout=20):
    """
    :param payload:  例如：{'user_id':1,'username':'wupeiqi'}用户信息
    :param timeout: token的过期时间，默认20分钟
    :return:
    """
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return result


def parse_payload(token):
    """
    对token进行和发行校验并获取payload
    :param token:
    :return:
    """
    result = {'status': False, 'data': None, 'error': None}
    try:
        verified_payload = jwt.decode(token, JWT_SALT, True)
        result['status'] = True
        result['data'] = verified_payload
    except jwt.exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result


class JwtQueryParamAuthentication(BaseAuthentication):
    """
    用户需要在url中通过参数进行传输token，例如：
    http://www.pythonav.com?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzM1NTU1NzksInVzZXJuYW1lIjoid3VwZWlxaSIsInVzZXJfaWQiOjF9.xj-7qSts6Yg5Ui55-aUOHJS4KSaeLq5weXMui2IIEJU
    """

    def authenticate(self, request):
        token = request.query_params.get('token')
        payload = parse_payload(token)
        if not payload['status']:
            raise exceptions.AuthenticationFailed(payload)

        # 如果想要request.user等于用户对象，此处可以根据payload去数据库中获取用户对象。
        return payload, token


class JwtAuthorizationAuthentication(BaseAuthentication):
    """
    用户需要通过请求头的方式来进行传输token，例如： Authorization:jwt
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzM1NTU1NzksInVzZXJuYW1lIjoid3VwZWlxaSIsInVzZXJfaWQiOjF9.xj
    -7qSts6Yg5Ui55-aUOHJS4KSaeLq5weXMui2IIEJU
    """

    def authenticate(self, request):

        # 非登录页面需要校验token
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        auth = authorization.split()
        if not auth:
            raise exceptions.AuthenticationFailed({'error': '未获取到Authorization请求头', 'status': False})
        if auth[0].lower() != 'jwt':
            raise exceptions.AuthenticationFailed({'error': 'Authorization请求头中认证方式错误', 'status': False})

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed({'error': "非法Authorization请求头", 'status': False})
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed({'error': "非法Authorization请求头", 'status': False})

        token = auth[1]
        result = parse_payload(token)
        # print(result)
        if not result['status']:
            raise exceptions.AuthenticationFailed(result)

        # 如果想要request.user等于用户对象，此处可以根据payload去数据库中获取用户对象。
        return result, token
