import re
from djdns.resolver import Resolver

def traverse(data, loader, query):
    '''
    data - page to start with
    loader - callback(uri) -> page data
    query - query text to scan for

    Generator that outputs branch dicts. You can filter recursion
    by having your loader function return None.
    '''
    for branch in data['branches']:
        selector = branch['selector']
        if re.search(selector, query):
            # Branch matches regex
            yield branch
            for b in _from_targets(branch, loader, query):
                yield b

def _from_targets(branch, loader, query):
    '''
    Generator that returns branches from a source branch's target.
    '''
    for target_uri in branch['targets']:
        target = loader(target_uri)

        if target == None:
            continue
        elif isinstance(target, Resolver):
            # Opaque resolver, such as dns:// URI.
            yield target
        else:
            # Registry page.
            for b in traverse(target, loader, query):
                yield b
