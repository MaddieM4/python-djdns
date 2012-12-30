import json
import re
from deje import document

import handlers

class Branch(object):
    def __init__(self, name=None, document = None):
        self.document = document or make_branch(name)
        self.document.branch_object = self
        self.name = self.document.name
        self.resource_path = "/djdns-branch"

    def own(self, owner):
        '''
        Set document owner object
        '''
        self.document.owner = owner

    def resolve(self, domain):
        self.compute_leads()
        for regex in self.leads_order:
            if re.match(regex, domain):
                return self.resolve_pointer(
                    domain,
                    self.leads_dict[regex]
                )
        raise KeyError("Domain %r did not match any regex" % domain)

    def resolve_pointer(self, domain, pointer):
        target = self.document.owner.load_document(pointer)
        target_branch = target.branch_object or Branch(None, target)
        return target_branch.resolve(domain)

    def compute_leads(self):
        if not self.leads_order or not self.leads_dict:
            self.leads_order = []
            self.leads_dict  = {}
            leads = self.leads
            for lead in leads:
                regex, pointer = lead
                self.leads_order.append(regex)
                self.leads_dict[regex] = pointer

    @property
    def content(self):
        return self.document.get_resource(self.resource_path).content

    @property
    def leads(self):
        return list(json.loads(self.content))

def make_branch(name):
    handler = handlers.branch()
    doc = document.Document(
        name,
        resources = [handler],
        handler_path = handler.path,
    )
    return doc
