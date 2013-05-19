from __future__ import print_function

import re
from pymads.sources.json import toRecord

class DJSource(object):
    '''
    Pymads Source that traverses DJDNS branches.

    root should be a dictlike object acting as the root DJDNS doc.

    loader should be a function that takes a target string, and returns another
    dictlike object (used for traversal). Blocking is fine.

    >>> from pymads.request import Request
    >>> from djdns.loaders.disk import DiskLoader
    >>> root = DiskLoader('diskdemo/root.json')
    >>> source = DJSource(root, DiskLoader)

    >>> r_root   = 'in.root.demo'
    >>> r_branch = 'in.subbranch.demo'
    >>> r_b3     = 'in.b3.demo'
    >>> r_none   = 'not.stored.in.demo'

    Testing a retrieval from the root document

    >>> a_root = source.get(r_root)
    >>> a_root #doctest: +ELLIPSIS
    [<pymads.record.Record object at ...>]
    >>> print(a_root[0].rdata)
    1.2.3.4
    >>> print(a_root[0].domain_name)
    in.root.demo

    Testing a traversed retrieval in a subbranch

    >>> a_branch = source.get(r_branch)
    >>> a_branch #doctest: +ELLIPSIS
    [<pymads.record.Record object at ...>]
    >>> print(a_branch[0].rdata)
    5.5.5.5
    >>> print(a_branch[0].domain_name)
    in.subbranch.demo

    Third branch of heirarchy.

    >>> a_b3 = source.get(r_b3)
    >>> a_b3 #doctest: +ELLIPSIS
    [<pymads.record.Record object at ...>]
    >>> print(a_b3[0].rdata)
    5.6.7.8
    >>> print(a_b3[0].domain_name)
    in.b3.demo

    Testing for a domain that isn't in the data at all

    >>> source.get(r_none)
    []
    '''
    def __init__(self, root, loader):
        self.root = root
        self.loader = loader

    def get(self, request, root = None):
        root = root or self.root

        for branch in root['branches']:
            selector = branch['selector']
            if re.search(selector, request):
                return self.resolve_from(request, branch)
        return []

    def resolve_from(self, request, branch):
        if branch['records']:
            return [toRecord(x, branch['selector']) for x in branch['records']]
        else:
            for target_uri in branch['targets']:
                target  = self.loader(target_uri)
                results = self.get(request, target)
                if results:
                    return results
            return []

    @property
    def branches(self):
        return self.root['branches']
