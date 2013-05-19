from __future__ import print_function

from pymads.server import DnsServer
from pymads.chain  import Chain

from djdns.source import DJSource
from djdns.loaders.disk import DiskLoader

class DJServer(DnsServer):
    def __init__(self, **config):
        if 'path' in config:
            self.path = config['path']
        else:
            self.path = './example.json'
        self.source = make_source(self.path)
        self.chain = Chain([self.source])
        config['chains'] = [self.chain]
        DnsServer.__init__(self, **config)

if __name__ == '__main__':
    server = DJDNS_Server(listen_port=8989)
    server.serve()
