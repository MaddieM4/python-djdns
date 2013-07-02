try:
    import urlparse
except:
    import urllib.parse as urlparse
import json

from pymads.sources.dns import MultiDNS

from djdns.resolver import ResolverWrapper

GLOBAL_MDNS = MultiDNS()

class DocLoader(object):
    '''
    Loads a page based on URI.
    '''

    def __init__(self, register_defaults = True, **kwargs):
        self.loaders = {}
        if register_defaults:
            self.register_defaults()
        self.register_dict(kwargs)

    def load(self, uri):
        parsed_uri = urlparse.urlparse(uri)
        scheme = parsed_uri.scheme

        if scheme in self.loaders:
            return self.loaders[scheme](parsed_uri)
        else:
            raise KeyError("No loader registered for scheme %r" % scheme)

    def register_dict(self, table):
        self.loaders.update(table)

    def register(self, name, callback):
        self.loaders[name] = callback

    def register_defaults(self):
        self.register_dict({
            'dns'  : dns_loader,
            'file' : file_loader,
            ''     : file_loader,
        })

def file_loader(parsed_uri):
    return json.load(open(parsed_uri.path))

def dns_loader(parsed_uri):
    hostname = parsed_uri.hostname
    port = int(parsed_uri.port or 53)

    server_addr = (hostname, port)

    return ResolverWrapper(
        GLOBAL_MDNS.get_source(server_addr)
    )
