#!/usr/bin/env python
# -*- utf-8 -*-

import jwt
import json
import datetime
import demjson
# from urllib.parse import parse_qs
from html import escape
# import os
from collections import namedtuple
from webob import Request, Response
from webob.dec import wsgify
import re
from webob.exc import HTTPTemporaryRedirect
from model.m import Router, Application
from functools import wraps

__KEY = 'sdfasdfasdfasdff'
router = Router()

router.route('/')
def main(ctx, request):
    return Response('hello world')

@router.route('/login', methods=['POST'])
def login(ctx, request):
    print('aaaaaaaaa')
    payload = json.loads(request.body.decode().replace("'", "\""))
    print(payload)
    if payload.get('username') == 'comyn' and payload.get('password') == 'pass':
        exp = datetime.datetime.utcnow() + datetime.timedelta(secondes=60)
        token = jwt.encode({'user': 'comyn', 'exp': exp}, __KEY, 'HS512').decode()
        return Response(json.dumps({'token': token}))
    return Response(json.dumps({'code': 401, 'message': 'username or password not match'}))






if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    application = Application()
    application.add_router(router)
    print(application.routers[0].routes)
    server = make_server('0.0.0.0', 3000, application)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()