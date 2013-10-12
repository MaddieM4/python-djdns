import os

from ejtp.util.compat import unittest
from ejtp.identity    import Identity, IdentityCache

from djdns.source    import DJSource
from djdns.traversal import traverse

class TestRegularTraversal(unittest.TestCase):
    # Port from doctest later
    pass

class TestUserTraversal(unittest.TestCase):
    def setUp(self):
        os.chdir('diskdemo')
        self.source = DJSource('root.json')

    def tearDown(self):
        os.chdir('..')

    def compareTraversal(self, domain, expected):
        traversal = traverse(
            self.source.root,
            self.source.load_user,
            domain
        )
        self.assertEqual(
            [x["selector"] for x in traversal],
            expected
        )

    def test_basic_traversal(self):
        self.compareTraversal(
            "example.org",
            ['example.org$']
        )

    def test_subbranch_traversal(self):
        self.compareTraversal(
            "in.subbranch.demo",
            ['(subbranch|b3).demo$','^in.subbranch.demo$']
        )
        
    def compareIdents(self, name, idents):
        self.assertEqual(
            sorted(self.source.get_user(name), key=lambda x: x.key),
            sorted(idents, key=lambda x: x.key)
        )
        
    def test_get_root_user(self):
        name      = "tom@example.org"
        encryptor = ["rotate", 5]
        location  = ["local", None, "tom"]

        ident = Identity(name, encryptor, location)
        self.compareIdents(name, [ident])

        name      = "jerry@example.org"
        encryptor = ["rotate", -5]
        location  = ["local", None, "jerry"]

        ident = Identity(name, encryptor, location)
        self.compareIdents(name, [ident])

    def test_get_subbranch_user(self):
        # Branch with many users
        # And they have a plan
        name    = "cylon@in.subbranch.demo"
        classes = ['centurion','humanoid','raider','hybrid']
        idents  = []
        for i in range(len(classes)):
            encryptor = ['rotate', i+1]
            location  = ['local', None, classes[i]]
            idents.append(Identity(name, encryptor, location))

        self.compareIdents(name, idents)
