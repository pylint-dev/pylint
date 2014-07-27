"""Functional full-module tests for PyLint."""
from __future__ import with_statement
import ConfigParser
import contextlib
import cStringIO
import operator
import os
import re
import sys

from logilab.common import testlib

from pylint import lint
from pylint import reporters
from pylint import checkers

class NoFileError(Exception):
    pass

# TODOs
#  - use a namedtuple for expected lines
#  - implement exhaustivity tests
#  - call skipTests in setUp when not using logilab.testlib any more.

# If message files should be updated instead of checked.
UPDATE = False

# Common sub-expressions.
_MESSAGE = {'msg': r'[a-z][a-z\-]+'}
# Matches a #,
#  - followed by a comparison operator and a Python version (optional),
#  - followed by an line number with a +/- (optional),
#  - followed by a list of bracketed message symbols.
# Used to extract expected messages from testdata files.
_EXPECTED_RE = re.compile(
    r'\s*#\s*(?:(?P<line>[+-]?[0-9]+):)?'
    r'(?:(?P<op>[><=]+) *(?P<version>[0-9.]+):)?'
    r'\s*\[(?P<msgs>%(msg)s(?:,\s*%(msg)s)*)\]' % _MESSAGE)


def parse_python_version(str):
    return tuple(int(digit) for digit in str.split('.'))


class TestReporter(reporters.BaseReporter):
    def add_message(self, msg_id, location, msg):
        self.messages.append(reporters.Message(self, msg_id, location, msg))

    def on_set_current_module(self, module, filepath):
        self.messages = []

    def display_results(self, layout):
        """Ignore layouts."""


class TestFile(object):
    """A single functional test case file with options."""

    _CONVERTERS = {
        'min_pyver': parse_python_version,
        'max_pyver': parse_python_version,
        'requires': lambda s: s.split(',')
    }


    def __init__(self, directory, filename):
        self._directory = directory
        self.base = filename.replace('.py', '')
        self.options = {
            'min_pyver': (2, 5),
            'max_pyver': (4, 0),
            'requires': []
            }
        self._parse_options()

    def _parse_options(self):
        cp = ConfigParser.ConfigParser()
        cp.add_section('testoptions')
        try:
            cp.read(self.option_file)
        except NoFileError:
            pass

        for name, value in cp.items('testoptions'):
            conv = self._CONVERTERS.get(name, lambda v: v)
            self.options[name] = conv(value)

    @property
    def option_file(self):
        return self._file_type('.rc')

    @property
    def module(self):
        package = os.path.basename(self._directory)
        return '.'.join([package, self.base])

    @property
    def expected_output(self):
        return self._file_type('.txt', check_exists=False)

    @property
    def source(self):
        return self._file_type('.py')

    def _file_type(self, ext, check_exists=True):
        name = os.path.join(self._directory, self.base + ext)
        if not check_exists or os.path.exists(name):
            return name
        else:
            raise NoFileError


_OPERATORS = {
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

def parse_expected_output(stream):
    lines = []
    for line in stream:
        parts = line.split(':', 3)
        if len(parts) != 4:
            symbol, lineno, obj, msg = lines.pop()
            lines.append((symbol, lineno, obj, msg + line))
        else:
            linenum = int(parts[1])
            lines.append((parts[0], linenum, parts[2], parts[3]))
    return lines


def get_expected_messages(stream):
    """Parses a file and get expected messages.

    :param stream: File-like input stream.
    :returns: A dict mapping line,msg-symbol tuples to the count on this line.
    """
    messages = {}
    for i, line in enumerate(stream):
        match = _EXPECTED_RE.search(line)
        if match is None:
            continue
        line = match.group('line')
        if line is None:
            line = i + 1
        elif line.startswith('+') or line.startswith('-'):
            line = i + 1 + int(line)
        else:
            line = int(line)

        version = match.group('version')
        op = match.group('op')
        if version:
            required = parse_python_version(version)
            if not _OPERATORS[op](sys.version_info, required):
                continue

        for msg_id in match.group('msgs').split(','):
            messages.setdefault((line, msg_id.strip()), 0)
            messages[line, msg_id.strip()] += 1
    return messages


def multiset_difference(left_op, right_op):
    """Takes two multisets and compares them.

    A multiset is a dict with the cardinality of the key as the value.

    :param left_op: The expected entries.
    :param right_op: Actual entries.

    :returns: The two multisets of missing and unexpected messages.
    """
    missing = left_op.copy()
    unexpected = {}
    for key, value in right_op.iteritems():
        missing.setdefault(key, 0)
        missing[key] -= value
        if missing[key] == 0:
            del missing[key]
        elif missing[key] < 0:
            unexpected.setdefault(key, 0)
            unexpected[key] = -missing.pop(key)
    return missing, unexpected


class LintModuleTest(testlib.TestCase):
    def __init__(self, test_file):
        super(LintModuleTest, self).__init__()
        test_reporter = TestReporter()
        self._linter = lint.PyLinter()
        self._linter.set_reporter(test_reporter)
        self._linter.config.persistent = 0
        checkers.initialize(self._linter)
        self._linter.disable('I')
        try:
            self._linter.load_file_configuration(test_file.option_file)
        except NoFileError:
            pass
        self._test_file = test_file

    def check_test(self):
        if (sys.version_info < self._test_file.options['min_pyver']
                or sys.version_info >= self._test_file.options['max_pyver']):
            self.skipTest(
                'Test cannot run with Python %s.' % (sys.version.split(' ')[0],))
        missing = []
        for req in self._test_file.options['requires']:
            try:
                __import__(req)
            except ImportError:
                missing.append(req)
        if missing:
            self.skipTest('Requires %s to be present.' % (','.join(missing),))

    def __str__(self):
        return "%s (%s.%s)" % (self._test_file.base, self.__class__.__module__, 
                               self.__class__.__name__)

    def _open_expected_file(self):
        return open(self._test_file.expected_output, 'U')

    def _get_expected(self):
        with open(self._test_file.source) as fobj:
            expected_msgs = get_expected_messages(fobj)

        if expected_msgs:
            with self._open_expected_file() as fobj:
                expected_output_lines = parse_expected_output(fobj)
        else:
            expected_output_lines = []
        return expected_msgs, expected_output_lines

    def _get_received(self):
        messages = self._linter.reporter.messages
        messages.sort(key=lambda m: (m.line, m.symbol, m.msg))
        received_msgs = {}
        received_output_lines = []
        for msg in messages:
            received_msgs.setdefault((msg.line, msg.symbol), 0)
            received_msgs[msg.line, msg.symbol] += 1
            received_output_lines.append(
                (msg.symbol, msg.line, msg.obj or '', msg.msg + '\n'))
        return received_msgs, received_output_lines

    def runTest(self):
        self.check_test()
        self._linter.check([self._test_file.module])

        expected_messages, expected_text = self._get_expected()
        received_messages, received_text = self._get_received()

        if expected_messages != received_messages:
            msg = ['Wrong results for file "%s":' % (self._test_file.base)]
            missing, unexpected = multiset_difference(expected_messages,
                                                      received_messages)
            if missing:
                msg.append('\nExpected in testdata:')
                msg.extend(' %3d: %s' % msg for msg in sorted(missing))
            if unexpected:
                msg.append('\nUnexpected in testdata:')
                msg.extend(' %3d: %s' % msg for msg in sorted(unexpected))
            self.fail('\n'.join(msg))
        self._check_output_text(expected_messages, expected_text, received_text)

    def _split_lines(self, expected_messages, lines):
        emitted, omitted = [], []
        for msg in lines:
            if (msg[1], msg[0]) in expected_messages:
                emitted.append(msg)
            else:
                omitted.append(msg)
        return emitted, omitted

    def _check_output_text(self, expected_messages, expected_lines, 
                           received_lines):
        self.assertSequenceEqual(
            self._split_lines(expected_messages, expected_lines)[0],
            received_lines)


class LintModuleOutputUpdate(LintModuleTest):
    def _open_expected_file(self):
        try:
            return super(LintModuleOutputUpdate, self)._open_expected_file()
        except IOError:
            return contextlib.closing(cStringIO.StringIO())

    def _check_output_text(self, expected_messages, expected_lines,
                           received_lines):
        if not expected_messages:
            return
        emitted, remaining = self._split_lines(expected_messages, expected_lines)
        if emitted != received_lines:
            remaining.extend(received_lines)
            remaining.sort(key=lambda m: (m[1], m[0], m[3]))
            with open(self._test_file.expected_output, 'w') as fobj:
                for line in remaining:
                    fobj.write('{0}:{1}:{2}:{3}'.format(*line))


def suite():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'functional')
    suite = testlib.TestSuite()
    for fname in os.listdir(input_dir):
        if fname != '__init__.py' and fname.endswith('.py'):
            test_file = TestFile(input_dir, fname)
            if UPDATE:
                suite.addTest(LintModuleOutputUpdate(test_file))
            else:
                suite.addTest(LintModuleTest(test_file))
    return suite


if __name__=='__main__':
    if '-u' in sys.argv:
        UPDATE = True
        sys.argv.remove('-u')
    testlib.unittest_main(defaultTest='suite')
