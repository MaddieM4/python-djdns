from ejtp.util.compat import unittest
from ejtp.tests.test_scripts import import_as_module, IOMock

class ScriptTester(unittest.TestCase):
    def _run(self, *argv, **kwargs):
        argv = [self.path] + argv
        with self.io:
            try:
                self.console.main(argv)
            except SystemExit:
                if not kwargs.get('error'):
                    raise
        return self.io.get_value()

    def setUp(self):
        self.io = IOMock()
        self.console = import_as_module(self.path)        

class TestMainScript(ScriptTester):
    path = 'djdns'

    def test_main(self):
        return True
