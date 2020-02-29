#!/usr/bin/env python
#-*- utf-8 -*-

from urllib.parse import parse_qs
from html import escape
import os
from webob import Request, Response


def application(environ, start_response):
    request = Request(environ)
    name = request.params.get('name', 'anon')
    body = 'hello {}'.format(escape(name))
    return Response(body)(environ, start_response)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 3000, application)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()