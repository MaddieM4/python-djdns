from __future__ import print_function

import re
from pymads.sources.json import toRecord

from djdns.loader   import DocLoader
from djdns.resolver import Resolver

class DJSource(Resolver):
    '''
    Pymads Source that traverses DJDNS branches.

    root should be a dictlike object acting as the root DJDNS doc.

    loader should be a function that takes a target string, and returns another
    dictlike object (used for traversal). Blocking is fine.

    >>> from pymads.request import Request
    >>> source = DJSource('diskdemo/root.json')

    >>> r_root   = 'in.root.demo'
    >>> r_branch = 'in.subbranch.demo'
    >>> r_b3     = 'in.b3.demo'
    >>> r_none   = 'not.stored.in.demo'

    Testing a retrieval from the root document

    >>> source.get_from_name(r_root) #doctest: +ELLIPSIS
    [<record for in.root.demo: 1800 A IN... 1.2.3.4>]

    Testing a traversed retrieval in a subbranch

    >>> source.get_from_name(r_branch) #doctest: +ELLIPSIS
    [<record for in.subbranch.demo: 1800 A IN... 5.5.5.5>]

    Third branch of heirarchy.

    >>> source.get_from_name(r_b3) #doctest: +ELLIPSIS
    [<record for in.b3.demo: 1800 A IN... 5.6.7.8>]

    Testing for a domain that isn't in the data at all

    >>> source.get_from_name(r_none)
    []

    Testing for recursive DNS domain

    >>> list(source.get_from_name('example.org')) #doctest: +ELLIPSIS
    [<record for example.org: ... A IN... ...>]

    '''
    def __init__(self, uri = "", loader = None, rootdata = None):
        self.uri = uri
        self.loader = loader or DocLoader()
        self.root = rootdata or self.load(self.uri)

    def load(self, uri):
        return self.loader.load(uri)

    def get(self, request, root = None):
        root = root or self.root

        for branch in root['branches']:
            selector = branch['selector']
            if re.search(selector, request.name):
                return self.resolve_from(request, branch)
        return []

    def resolve_from(self, request, branch):
        if branch['records']:
            return [toRecord(x, branch['selector']) for x in branch['records']]
        else:
            for target_uri in branch['targets']:
                target  = self.load(target_uri)
                if isinstance(target, Resolver):
                    results = target.get(request)
                else:
                    results = self.get(request, target)
                if results:
                    return results
            return []

    @property
    def branches(self):
        return self.root['branches']
