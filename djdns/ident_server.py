try:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from http.server import HTTPServer, BaseHTTPRequestHandler

import json
import socket
from ejtp.identity import IdentityCache

INTRO_TEXT = '''
<!DOCTYPE html>
<html>
<head>
    <title>DJDNS Identity Retrieval Interface</title>
</head>
<body>
<h2>This is the DJDNS Identity Retrieval Interface.</h2>

<p>To use it, go to /idents/name@domain.com, filling in with the 
address of the actual person you want. You'll get a JSON response back,
with all the info we can find. If we can't find anything, the content
will just be an empty cache ({}) and the status code will be 404.</p>

<p>Depending on the dataset this server is running on, one or more of
the following links will probably work for you.</p>

<ul>
    <li><a href="/idents/tom@example.org">Diskdemo example</a></li>
    <li><a href="/idents/cylon@in.subbranch.demo">Diskdemo example 2</a></li>
    <li><a href="/idents/philip@roaming-initiative.com">Public registry (real) example</a></li>
</ul>

<p>For more information, see <a href="https://github.com/campadrenalin/python-djdns/blob/master/docs/IDENTITY_REGISTRATION.md">the documentation.</a></p>

</body>
</html>
'''

NOT_FOUND_TEXT = '''
<!DOCTYPE html>
<html>
<head>
    <title>Not found</title>
</head>
<body>
<h2>404 Not Found</h2>

<p>Sorry.</p>
</html>
'''

class Handler(BaseHTTPRequestHandler):

    def result(self, code, content_type, data):
        self.send_response(code)
        self.send_header('Content-type', content_type+'; charset=utf-8')
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == '/':
            return self.intro()
        elif self.path.startswith('/idents/'):
            return self.get_ident(self.path[8:])
        else:
            return self.not_found()

    def intro(self):
        return self.result(200, 'text/html', INTRO_TEXT)

    def get_ident(self, name):
        cache = IdentityCache()
        cache.update_idents(self.source.get_user(name))

        if len(cache.all()) > 0:
            status = 200
        else:
            status = 404

        payload = json.dumps(cache.serialize())
        if bytes != str:
            payload = bytes(payload, 'utf-8')
        return self.result(status, 'application/json', payload)

    def not_found(self):
        return self.result(404, 'text/html', NOT_FOUND_TEXT)

    @property
    def source(self):
        return self.server.parent.source

class HTTPServerIPv6(HTTPServer):
    address_family = socket.AF_INET6

class IdentServer(object):
    def __init__(self, source, host='::', port=16232):
        self.source = source
        self.serving = False
        self.addr = (host, port)
        self.server = HTTPServerIPv6(self.addr, Handler)
        self.server.parent = self

    def __repr__(self):
        return "<djdns IdentServer on '{0}':{1}>".format(*self.addr)

    def serve(self):
        self.serving = True
        while self.serving:
            self.server.handle_request()
        self.server.server_close()

    def stop(self):
        self.serving = False

def serve_standalone():
    from djdns.source import DJSource
    import os
    os.chdir('diskdemo')
    server = IdentServer(DJSource('root.json'))
    try:
        server.serve()
    except KeyboardInterrupt:
        server.stop()

if __name__ == '__main__':
    serve_standalone()
