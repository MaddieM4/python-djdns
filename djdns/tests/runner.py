import os
import sys
from ejtp.util.compat import unittest

def main():
    loader = unittest.TestLoader()
    if len(sys.argv) > 1:
        tests = unittest.TestSuite()
        names = sys.argv[1:]
        for name in names:
            try:
                test = loader.loadTestsFromName('%s.%s' % (__package__, name))
            except AttributeError as ex:
                print("Error loading '%s': %s" % (name, ex))
                quit(1)
            tests.addTests(test)
    else:
        base_path = os.path.split(__file__)[0]
        tests = loader.discover(base_path)
    test_runner = unittest.runner.TextTestRunner()
    results = test_runner.run(tests)
    if not results.wasSuccessful():
        quit(1)

if __name__ == '__main__':
    main()
