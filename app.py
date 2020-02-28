#!/usr/bin/env python
#-*- coding:utf-8 -*-

from urllib.parse import parse_qs
from html import escape

def application(environ, start_response):
    params = parse_qs(environ.get('QUERY_STRING'))
    name = params.get('NAME', ['anon'])[0]

    body = 'hello {}'.format(name)
    status = '200 OK'
    headers = [
        ('content-type', 'text/plain'),
        ('content-length', str(len(body)))
    ]
    start_response(status, headers)
    return [body.encode()]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 3000, application)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

