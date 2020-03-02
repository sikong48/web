#!/usr/bin/env python
# -*- utf-8 -*-

# from urllib.parse import parse_qs
from html import escape
# import os
from collections import namedtuple
from webob import Request, Response
from webob.dec import wsgify
import re
from webob.exc import HTTPTemporaryRedirect
from model.m import Router, Application



router1 = Router(domain='python.magedu.com')
router2 = Router('/r2')


@router2.route('/hello/{name}/{age:int}')
def hello(application, request):
    print(request.args['age'])
    print(type(request.args['age']))
    name = request.params.get('name', 'anon')
    body = 'hello, {} is {} years old.'.format(request.args['name'], request.args['age'])
    return Response(body)


@router1.route(r'/favicon.ico$')
def favicon(application, request):
    with open('favicon.ico', 'rb') as f:
        resp = Response(body=f.read(), content_type='image/x-icon')
        return resp


@router1.route(r'/')
def main(application, request):
    #if application.options.get('debug'):
    #    for k, v in request.headers.items():
    #        print('{} => {}'.format(k, v))
    #return Response("this is a man page")
    raise HTTPTemporaryRedirect(location='/r2/hello/xxx/111')


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    application = Application()
    application.add_router(router1)
    application.add_router(router2)
    print(router2.routes)
    server = make_server('0.0.0.0', 3000, application)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()