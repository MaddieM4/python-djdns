class Resolver(object):
    '''
    Taxonomical class for objects that fulfill Resolver interface.
    '''

    def get(self, domain_name):
        '''
        Takes domain name, returns array of pymads records.
        '''
        raise NotImplementedError('Resolver subclass must define get()')

class ResolverWrapper(Resolver):
    '''
    Wrap an object that already fulfills Resolver interface, but isn't
    a subclass of Resolver.
    '''

    def __init__(self, source):
        self.source = source

    def get(self, domain_name):
        return self.source.get(domain_name)
