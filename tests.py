import mock
import os
import shutil
import subprocess

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from shell import CommandError, Shell, shell


class ShellTestCase(unittest.TestCase):
    def setUp(self):
        super(ShellTestCase, self).setUp()
        self.test_dir = os.path.join('/tmp', 'python_shell')
        self.hello_path = os.path.join(self.test_dir, 'hello.txt')
        self.sh = Shell()

        shutil.rmtree(self.test_dir, ignore_errors=True)
        os.makedirs(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        super(ShellTestCase, self).tearDown()

    def test_initialization(self):
        sh = Shell()
        self.assertFalse(sh.has_input)
        self.assertTrue(sh.record_output)
        self.assertTrue(sh.record_errors)
        self.assertEqual(sh.last_command, '')
        self.assertEqual(sh.line_breaks, '\n')
        self.assertEqual(sh.code, 0)
        self.assertEqual(sh._popen, None)

        sh = Shell(has_input=True, record_output=False, record_errors=False)
        self.assertTrue(sh.has_input)
        self.assertFalse(sh.record_output)
        self.assertFalse(sh.record_errors)

    def test__split_command(self):
        self.assertEqual(self.sh._split_command('ls'), ['ls'])
        self.assertEqual(self.sh._split_command('ls -alh *.py'), ['ls', '-alh', '*.py'])
        self.assertEqual(self.sh._split_command(['ls', '-alh']), ['ls', '-alh'])

    def test__handle_output_simple(self):
        sh = Shell()
        self.assertEqual(sh._stdout, '')
        self.assertEqual(sh._stderr, '')

        sh._handle_output('another.txt\n', None)
        self.assertEqual(sh._stdout, 'another.txt\n')
        self.assertEqual(sh._stderr, '')

        sh._handle_output('something.txt\n', 'Error: Please supply an arg.\n')
        self.assertEqual(sh._stdout, 'another.txt\nsomething.txt\n')
        self.assertEqual(sh._stderr, 'Error: Please supply an arg.\n')

    def test__handle_output_norecord(self):
        sh = Shell(record_output=False, record_errors=False)
        self.assertEqual(sh._stdout, '')
        self.assertEqual(sh._stderr, '')

        sh._handle_output('another.txt\n', 'Error: Please supply an arg.')
        self.assertEqual(sh._stdout, '')
        self.assertEqual(sh._stderr, '')

    def test__communicate(self):
        def fake_communicate(input=None):
            self.sh._popen.returncode = 1
            return ('whatever\n', 'An error')

        self.assertEqual(self.sh._stdout, '')
        self.assertEqual(self.sh._stderr, '')
        self.assertEqual(self.sh.code, 0)
        self.sh._popen = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        with mock.patch.object(self.sh._popen, 'communicate', fake_communicate) as mock_communicate:
            self.sh._communicate()
            self.assertEqual(self.sh._stdout, 'whatever\n')
            self.assertEqual(self.sh._stderr, 'An error')
            self.assertEqual(self.sh.code, 1)
            self.assertNotEqual(self.sh.pid, 0)

    def test_run(self):
        self.assertFalse(os.path.exists(self.hello_path))

        self.sh.run('touch %s' % self.hello_path)
        self.assertTrue(os.path.exists(self.hello_path))
        self.assertEqual(self.sh.code, 0)

    def test_stdout(self):
        with open(os.path.join(self.test_dir, 'another.txt'), 'w') as another:
            another.write('Whatev.')

        self.sh.run('ls %s' % self.test_dir)
        self.assertEqual(self.sh.code, 0)
        self.assertEqual(self.sh.output(), ['another.txt'])

        # Now with the raw output.
        self.assertEqual(self.sh.output(raw=True), 'another.txt\n')

    def test_stderr(self):
        self.sh.run('ls /there-s-no-way-anyone/has/this/directory/please')
        self.assertEqual(self.sh.code, 1)
        self.assertTrue('No such file' in self.sh.errors()[0])

        # Now with the raw errors.
        self.assertTrue('No such file' in self.sh.errors(raw=True))

    def test_write(self):
        sh = Shell(has_input=True)
        sh.run('cat -u')
        sh.write('TEH INPUTS')
        self.assertEqual(sh.output(), ['TEH INPUTS'])
        self.assertEqual(sh.code, 0)

    # TODO: This test is flawed. Not sure how to implement it with kill.
    # def test_kill(self):
    #     spin = subprocess.Popen('sleep 10 && echo "done" &', stdout=subprocess.PIPE)
    #     spin.poll()
    #
    #     self.sh._popen = spin
    #
    #     self.sh.kill()
    #     self.assertEqual(self.sh.code, 1)

    def test_shortcut_interface(self):
        self.assertFalse(os.path.exists(self.hello_path))

        sh = shell('touch %s' % self.hello_path)
        self.assertTrue(os.path.exists(self.hello_path))
        self.assertEqual(sh.code, 0)

    def test_chaining(self):
        sh = Shell(has_input=True)
        output = sh.run('cat -u').write('Hello, world!').output()
        self.assertEqual(output, ['Hello, world!'])

        output = shell('cat -u', has_input=True).write('Hello, world!').output()
        self.assertEqual(output, ['Hello, world!'])

    def test_die(self):
        sh = Shell(die=True)
        with self.assertRaises(CommandError):
            sh.run('ls /maybe/this/exists/on/windows/or/something/idk')
        try:
            no_die = shell('ls /other/fake/stuff/for/sure')  # get the stderr
            sh.run('ls /other/fake/stuff/for/sure')
        except CommandError, e:
            self.assertEqual(e.code, 1)
            self.assertEqual(e.stderr, no_die.errors()[0] + os.linesep)

