#!/usr/bin/env python
# -*- utf-8 -*-

# from urllib.parse import parse_qs
from html import escape
# import os
from collections import namedtuple
from webob import Request, Response
from webob.dec import wsgify
import re

RULES = {
    'str': '[^/].+',
    'word': '\w+',
    'any': '.+',
    'int': '[+-]?\d+',
    'float': '[+-]?\d+\.\d+'
}

CASTS = {
    'str': str,
    'word': str,
    'any': str,
    'int': int,
    'float': float
}


Route = namedtuple('Route', ['rule', 'methods', 'casts', 'handler'])


class Router:
    def __init__(self, prefix='', domain=None):
        self.routes = []
        self.domain = domain
        self.prefix = prefix

    def _route(self, rule, methods, handler):
        rule, casts = self._rule_parse(rule)
        self.routes.append(Route(re.compile(rule), methods, casts, handler))

    def _rule_parse(self, rules):
        rule = []
        spec = []
        casts = {}
        is_spec = []
        for c in rules:
            if c == '{' and not is_spec:
                is_spec = True
            elif c == '}' and is_spec:
                is_spec = False
                name, r, c = self._spec_parse(''.join(spec))
                spec = []
                rule.append(r)
                casts[name] = c
            elif is_spec:
                spec.append(c)
            else:
                rule.append(c)
        return '{}$'.format(''.join(rule)), casts


    def _spec_parse(self, src):
        tmp = src.split(':')
        if len(tmp) > 2:
            raise Exception('error parttern')
        name = tmp[0]
        type = 'str'
        if len(tmp) == 2:
            type = tmp[1]
        rule = '(?P<{}>{})'.format(name, RULES[type])
        return name, rule, CASTS[type]

    def route(self, rule, methods=None):
        if methods is None:
            methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTION')

        def dec(handler):
            self._route(rule, methods, handler)
            return handler
        return dec

    def _domain_match(self, request):
        return self.domain is None or re.match(self.domain, request.host)
    def _prefix_match(self, request):
        return request.path.startswith(self.prefix)

    def match(self, request):
        if self._domain_match(request) and self._prefix_match(request):
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
            if handler:
                return handler(self, request)


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
    if application.options.get('debug'):
        for k, v in request.headers.items():
            print('{} => {}'.format(k, v))
    return Response("this is a man page")


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