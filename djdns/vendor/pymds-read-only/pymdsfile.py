# Copyright (c) 2009 Tom Pinckney
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
#     The above copyright notice and this permission notice shall be
#     included in all copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#     EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#     OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#     NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT


#
# A pymds source filter.
#
# pymdsfile answers queries by consulting a text database.
#
# initializer: a single argument specifying the name of the database
# file.  See the example pinckney.com.txt database for documentation
# on the format of this file.
#

import struct

from utils import *

class Source(object):
    def __init__(self, filename):
        self._answers = {}
        self._filename = filename
        self._parse_file()

    def _parse_file(self):
        f = open(self._filename, "r")
        for line in f.readlines():
            line = line.strip()        
            if line and line[0] != '#':
                question, type, value = line.split()
                question = question.lower()
                type = type.upper()
                if question == '@':
                    question = ''
                if type == 'A':
                    answer = struct.pack("!I", ipstr2int(value))
                    qtype = 1
                if type == 'NS':
                    answer = labels2str(value.split("."))
                    qtype = 2
                elif type == 'CNAME':
                    answer = labels2str(value.split("."))
                    qtype = 5
                elif type == 'TXT':
                    answer = label2str(value)
                    qtype = 16
                elif type == 'MX':
                    preference, domain = value.split(":")
                    answer = struct.pack("!H", int(preference))
                    answer += labels2str(domain.split("."))
                    qtype = 15
                self._answers.setdefault(question, {}).setdefault(qtype, []).append(answer)
        f.close()

    def get_response(self, query, domain, qtype, qclass, src_addr):
        if query not in self._answers:
            return 3, []
        if qtype in self._answers[query]:
            results = [{'qtype': qtype, 'qclass':qclass, 'ttl': 500, 'rdata': answer} for answer in self._answers[query][qtype]]
            return 0, results
        elif qtype == 1:
            # if they asked for an A record and we didn't find one, check for a CNAME
            return self.get_response(query, domain, 5, qclass, src_addr)
        else:
            return 3, []
