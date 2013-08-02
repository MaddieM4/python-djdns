from ejtp.util.compat import unittest
from subprocess import Popen, PIPE
import time

try:
    from cStringIO import StringIO
except:
    from io import BytesIO as StringIO

class ExternalScriptError(Exception): pass

class ScriptTester(object):

    def __init__(self, path, argv):
        self.path = path
        self.argv = [self.path] + list(argv)
        self.io_stdin  = StringIO()
        self.io_stdout = StringIO()
        self.io_stderr = StringIO()
        self.io_output = StringIO()

    def write(self, input):
        self.io_stdin.write(input)
        return self.process.stdin.write(input)

    def read(self):
        out = self.process.stdout.read()
        err = self.process.stderr.read()

        self.io_stdout.write(out)
        self.io_stderr.write(err)
        self.io_output.write(out)
        self.io_output.write(err)

        return (out, err)

    @property
    def stdin(self):
        return self.io_stdin.getvalue()

    @property
    def stderr(self):
        return self.io_stderr.getvalue()

    @property
    def stdout(self):
        return self.io_stdout.getvalue()

    @property
    def output(self):
        return self.io_output.getvalue()

    def __enter__(self):
        self.process = Popen(self.argv, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if not self.process.poll():
            try:
                self.process.terminate()
            except:
                pass # harmless race condition
        returncode = self.process.wait()
        self.process = None
        if returncode and exc_value == None:
            raise ExternalScriptError(returncode, self.io_output.getvalue())

class TestMainScript(unittest.TestCase):
    path = 'djdns'

    def test_main(self):
        args = [
            '-d', 'diskdemo',
            '-P', '4444',
        ]
        try:
            with ScriptTester(self.path, args) as p:
                stderr = "stuff"
                while stderr:
                    (stdout, stderr) = p.read()
                self.assertEqual(p.output, bytes())
        except ExternalScriptError:
            pass
