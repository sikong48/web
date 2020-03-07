#!/usr/bin/env python
# -*- utf-8 -*-

from model.m import Router, Application
from webob import Response
from functools import wraps
from base64 import b64decode
from webob.exc import HTTPUnauthorized


router = Router()

def authenticated(fn):
    @wraps(fn)
    def wrap(ctx, request):
        header = request.headers.get('Authorization')
        if header is None:
            raise HTTPUnauthorized()
        user, password = b64decode(header.split()[-1].encode()).decode().split(':')
        if user == 'comyn' and password == 'pass':
            request.user = user
            return fn(ctx, request)
        raise HTTPUnauthorized()
    return wrap




@router.route('/')
@authenticated
def main(ctx, request):
    return Response('hello worldfffffbbbbbbbbbbbbbbbbbbb')

app = Application([router])

if __name__ == '__main__':
    app = Application()
    app.add_router(router)
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 3000, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()