from __future__ import unicode_literals
from ejtp.util.compat import unittest
from pymads.tests.dig import dig

import signal
import time
from subprocess import Popen, PIPE

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

        self.returncode = None

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

    def terminate(self):
        '''
        Stop process and return after wait.
        '''
        if self.returncode != None:
            return
        if not self.process.poll():
            try:
                self.process.send_signal(signal.SIGINT)
            except:
                pass # harmless race condition
        self.returncode = self.process.wait()
        self.read()

    def __enter__(self):
        self.process = Popen(self.argv, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.terminate()
        self.process = None
        if self.returncode and exc_value == None:
            raise ExternalScriptError(
                self.returncode,
                self.io_output.getvalue()
            )

class TestMainScript(unittest.TestCase):
    path = 'djdns'

    def test_runs_at_all(self):
        args = [
            '-d', 'diskdemo',
            '-P', '4444',
        ]
        with ScriptTester(self.path, args) as p:
            time.sleep(1)
            p.terminate()
            self.assertEqual(
                p.output,
                b"STOPPING SERVER <pymads dns serving on ('::', 0, 1):4444>\n"
            )
            self.assertEqual(p.returncode, 0)

    def test_resolution(self):
        port = 4444
        args = [
            '-d', 'diskdemo',
            '-P', str(port),
        ]
        with ScriptTester(self.path, args) as p:
            host_data = dig('in.root.demo', 'localhost', port)
            expected = "ANSWER SECTION:\n%s.\t\t1800\tIN\tA\t%s\n\n" % (
                'in.root.demo',
                '1.2.3.4',
            )
            self.assertIn(expected, host_data)
