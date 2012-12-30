#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'djdns',
    version = '0.0.1',
    description = 'DEJE-based authoritative DNS server',
    author = 'Philip Horger',
    author_email = 'philip.horger@gmail.com',
    url = 'https://github.com/campadrenalin/python-djdns/',
    scripts = [
        #'scripts/djdns',
    ],
    packages = [
        'djdns',
         #'djdns.vendor',
    ],
)

