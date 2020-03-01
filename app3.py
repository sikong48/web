#!/usr/bin/env python
#-*- utf-8 -*-

from urllib.parse import parse_qs
from html import escape
import os
from webob import Request, Response
from webob.dec import wsgify

@wsgify
def application(request):
    if request.path == '/favicon.ico':
        return favicon(request)
    if request.path.startswith('/hello'):
        return hello(request)
    if request.path.startswith('/'):
        return main(request)

def main(request):
    return Response("this is a man page")
def hello(request):
    name = request.params.get('name', 'anon')
    body = 'hello {}'.format(escape(name))
    return Response(body)
def favicon(request):
    with open('favicon.ico', 'rb') as f:
        resp = Response(body=f.read(), content_type='image/x-icon')
        return resp


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 3000, application)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()