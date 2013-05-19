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

    >>> r_root   = Request(0, ['in','root','demo'], 0,0, None) # in.root.demo
    >>> r_branch = Request(0, ['in','subbranch','demo'], 0,0, None) # in.subbranch.demo
    >>> r_none   = Request(0, ['not','stored','in','demo'], 0,0, None) # not.stored.in.demo

    >>> source.get(r_root)
    []
    >>> source.get(r_branch)
    []
    >>> source.get(r_none)
    []
    '''
    def __init__(self, root, loader):
        self.root = root
        self.loader = loader

    def get(self, request, root = None):
        root = root or self.root
        name = request.name

        for branch in self.branches:
            selector = branch['selector']
            if re.search(selector, name):
                return self.resolve_from(request, branch)
        return []

    def resolve_from(self, request, branch):
        if branch['records']:
            return [toRecord(x, branch['selector']) for x in branch['records']]
        else:
            for target_uri in branch['targets']:
                target  = self.loader(target_uri)
                results = self.get(target)
                if results:
                    return results
            return []

    @property
    def branches(self):
        return self.root['branches']
