#!/usr/bin/env python
#-*- coding:utf-8 -*-

from urllib.parse import parse_qs
from html import escape

class Request:
#    params = parse_qs(environ.get('QUERY_STRING'))
#    name = params.get('NAME', ['anon'])[0]
    def __init__(self, environ):
        self.params = parse_qs(environ.get('QUERY_STRING'))

class Response:
    STATUS = {
        200: 'OK',
        404: 'Not found'
    }
    def __init__(self, body=None):
        self.body = body
        self.status = '200 OK'
        self.headers = {

        }
    def set_body(self, body):
        self.body = body
        self.headers['content-length'] = str(len(self.body))
    def set_status(self, status_code, status_test):
        self.status = '{} {}'.format(status_code, status_test)
    def set_headers(self, name, value):
        self.headers[name] = value

    def __call__(self, start_response):
        start_response(self.status, [(k, v) for k, v in self.headers.items()])
        return [self.body.encode()]


def application(environ, start_response):
    request = Request(environ)
    name = request.params.get('name', ['anon'])[0]
    body = 'hello {}'.format(escape(name))
    return Response(body)(start_response)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 3000, application)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()