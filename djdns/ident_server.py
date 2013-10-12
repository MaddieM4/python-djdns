import bottle
import json

from ejtp.identity import IdentityCache

class IdentServer(object):
    def __init__(self, source, **kwargs):
        self.bottle = bottle.Bottle()
        self.bottle.route('/idents/:name', self.get_ident)
        self.config = kwargs

    def serve(self):
        self.bottle.run(**self.config)

    def get_ident(self, name):
        cache = IdentityCache()
        cache.update_idents(self.source.get_user(name))

        if len(cache.all()):
            status = 200
        else:
            status = 404

        return bottle.Response(
            json.dumps(cache.serialize()),
            status,
            content_type='application/json'
        )

def serve_standalone():
    from djdns.source import DJSource
    server = IdentServer(DJSource('diskdemo/root.json'), port=8959)
    server.serve()

if __name__ == '__main__':
    serve_standalone()
