from pymads.request import Request

class Resolver(object):
    '''
    Taxonomical class for objects that fulfill Resolver interface.
    '''

    def get(self, request):
        '''
        Takes pymads Request, returns array of pymads records.
        '''
        raise NotImplementedError('Resolver subclass must define get()')

    def get_from_name(self, domain_name):
        '''
        Takes domain name, returns array of pymads records.
        '''
        request = Request()
        request.name = domain_name
        return self.get(request)

class ResolverWrapper(Resolver):
    '''
    Wrap an object that already fulfills Resolver interface, but isn't
    a subclass of Resolver.
    '''

    def __init__(self, source):
        self.source = source

    def get(self, request):
        return self.source.get(request)
