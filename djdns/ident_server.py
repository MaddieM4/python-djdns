import bottle
import json

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

</body>
</html>
'''

class IdentServer(object):
    def __init__(self, source, **kwargs):
        self.source = source
        self.bottle = bottle.Bottle()
        self.bottle.route('/', callback=self.intro)
        self.bottle.route('/idents/:name', callback=self.get_ident)
        self.config = kwargs

    def serve(self):
        self.bottle.run(**self.config)

    def intro(self):
        return [INTRO_TEXT]

    def get_ident(self, name):
        cache = IdentityCache()
        cache.update_idents(self.source.get_user(name))

        if len(cache.all()) > 0:
            bottle.response.status = 200
        else:
            bottle.response.status = 404

        return cache.serialize()

def serve_standalone():
    from djdns.source import DJSource
    server = IdentServer(DJSource('diskdemo/root.json'), port=8959)
    server.serve()

if __name__ == '__main__':
    serve_standalone()
