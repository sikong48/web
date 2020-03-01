#!/usr/bin/env python
# -*- utf-8 -*-

# from urllib.parse import parse_qs
from html import escape
# import os
from collections import namedtuple
from webob import Request, Response
from webob.dec import wsgify
import re


Route = namedtuple('Route', ['rule', 'methods', 'handler'])


class Router:
    def __init__(self, prefix='', domain=None):
        self.routes = []
        self.domain = domain
        self.prefix = prefix

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
        if self.domain is None or re.match(self.domain, request.host):
            if request.path.startswith(self.prefix):
                for route in self.routes:
                    if request.method in route.methods:
                        m = route.rule.match(request.path.replace(self.prefix, '', 1))
                        if m:
                            request.args = m.groupdict()
                            return route.handler



class Application:
    def __init__(self, **options):
        self.routers = []
        self.options = options

    def add_router(self, router):
        self.routers.append(router)

    @wsgify
    def __call__(self, request):
        for router in self.routers:
            handler = router.match(request)
            print(handler)
            if handler:
                return handler(self, request)


router1 = Router(domain='python.magedu.com')
router2 = Router('/r2')


@router2.route(r'/hello$')
def hello(application, request):
    name = request.params.get('name', 'anon')
    body = 'hello {}'.format(escape(name))
    return Response(body)


@router1.route(r'/favicon.ico$')
def favicon(application, request):
    with open('favicon.ico', 'rb') as f:
        resp = Response(body=f.read(), content_type='image/x-icon')
        return resp


@router1.route(r'/')
def main(application, request):
    if application.options.get('debug'):
        for k, v in request.headers.items():
            print('{} => {}'.format(k, v))
    return Response("this is a man page")


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    application = Application()
    application.add_router(router1)
    application.add_router(router2)
    print(application.routers)
    print(router1.routes)
    print(router2.routes)
    server = make_server('0.0.0.0', 3000, application)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()