import string
import socket
import random
import re

from utils import *

class Filter(object):
    def __init__(self, overrides_file):
	self.overrides = {}

	# Let's preconfigure some regexes we'll use to parse the config...
	linesplitter = re.compile('''
	([^#:]*)		# Match the IPv6 prefix (eg. 2001-0db8-aaaa-bb)
	\s*			# Some optional whitespace
	:			# Delimiter
	\s*			# Some more optional whitespace
	\{			# Start of nameserver list
		\s*		# More optional whitespace
		([^#}]*)	# Any non-comment set of nameservers
				# (comma-separated but we don't look at that yet)
		\s*		# Even more optional whitespace again
	\}			# End of nameserver list
	''', re.VERBOSE)

	# A regex that matches anything that isn't whitespace or a comma
	nsgrabber = re.compile('[^,\s]+')

	f = open (overrides_file, 'r')
	for l in f:
		# Start splitting the line...
		data = linesplitter.match(l)

		# Ignore empty or malformed lines...
		if data == None: continue

		# Pull out the IPv6 network prefix to override for
		# and make it a reverse-zone-style list & tuple
		ip6prefix = list(data.group(1).replace('-',''))
		ip6prefix.reverse()
		ip6prefix += ['ip6', 'arpa']
		t_ip6prefix = tuple(ip6prefix)

		# Pull out the list of nameservers
		# (cleaning out/splitting by commas and whitespace)
		nameservers = nsgrabber.findall(data.group(2))

		# Build up the override list
		# (we use a tuple as lists aren't hashable)
		self.overrides[t_ip6prefix] = []
		for nameserver in nameservers:
			nameserver = nameserver.strip()
			print "Added %s for %s" % (nameserver, ip6prefix)
			self.overrides[t_ip6prefix] += [{
				'qtype': 2,
				'qclass': 1,
				'question': ip6prefix,
				'ttl': 86400,
				'rdata': labels2str(nameserver.split('.'))
			}]
	f.close()

    def filter(self, query, domain, qtype, qclass, src_addr, an_resource_records, ns_resource_records):
	print "Running filter for %s.%s (qtype=%s)" % (query, domain, qtype)
	# Check for possible overrides. Start with the most specific
	# query we have (in case we're overriding a /128 lookup) and
	# progress until we'd be checking our zone itself.
	t_full_query = tuple(query + domain)
	while len(t_full_query) > len(domain):
		print "*** Checking for", t_full_query
		if t_full_query in self.overrides:
                	print "Returning %s instead of %s" % (self.overrides[t_full_query], an_resource_records)
			# Be nice to delegated nameservers
			random.shuffle (self.overrides[t_full_query])
                	return [], self.overrides[t_full_query]
		t_full_query=t_full_query[1:]

	# Didn't find an override; let's return what we were given unchanged.
        return an_resource_records, ns_resource_records

