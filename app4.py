#!/usr/bin/env python
#-*- utf-8 -*-

from urllib.parse import parse_qs
from html import escape
import os
from webob import Request, Response
from webob.dec import wsgify
import re

#@wsgify
#def application(request):
#    if re.match(r'/favicon.ico$', request.path):
#        return favicon(request)
#    if re.match(r'/hello$', request.path):
#        return hello(request)
#    if re.match(r'/', request.path):
#        return main(request)

class Application:
    def __init__(self):
        self.routers = []
    def route(self, rule, handler):
        self.routers.append((rule, handler))
    @wsgify
    def __call__(self, request):
        for rule, handler in self.routers:
            if re.match(rule, request.path):
                return handler(request)

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
    application = Application()
    application.route(r'favicon.ico$', favicon)
    application.route(r'/hello$', hello)
    application.route(r'/', main)
    server = make_server('0.0.0.0', 3000, application)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()