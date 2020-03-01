#!/usr/bin/env python
# -*- utf-8 -*-

from urllib.parse import parse_qs
from html import escape
import os
from collections import namedtuple
from webob import Request, Response
from webob.dec import wsgify
import re

Route = namedtuple('Route', ['rule', 'methods', 'handler'])


class Router:
    def __init__(self):
        self.routes = []

    def _route(self, rule, methods, handler):
        self.routes.append(Route(re.compile(rule), methods, handler))

    def route(self, rule, methods=None):
        if methods is None:
            methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTION')

        def dec(handler):
            self._route(rule, methods, handler)
            return handler
        return dec

    def match(self, request):
        pass

route = Router()

class Application:
    def __init__(self, **options):
        self.routers = []
        self.options = options

    def set_routers(self, router):
        self.routers = router

    @wsgify
    def __call__(self, request):
        for route in self.routers:
            if request.method in route.methods:
                if route.rule.match(request.path):
                    return route.handler(self, request)





@route.route(r'/hello$')
def hello(application, request):
    name = request.params.get('name', 'anon')
    body = 'hello {}'.format(escape(name))
    return Response(body)


@route.route(r'/favicon.ico$')
def favicon(application, request):
    with open('favicon.ico', 'rb') as f:
        resp = Response(body=f.read(), content_type='image/x-icon')
        return resp


@route.route(r'/')
def main(application, request):
    if application.options.get('debug'):
        for k, v in request.headers.items():
            print('{} => {}'.format(k, v))
    return Response("this is a man page")


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    application = Application()
    application.set_routers(route.routes)
    server = make_server('0.0.0.0', 3000, application)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()