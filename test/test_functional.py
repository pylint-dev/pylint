"""Functional full-module tests for PyLint."""
from __future__ import with_statement
import ConfigParser
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
    }


    def __init__(self, directory, filename):
        self._directory = directory
        self.base = filename.replace('.py', '')
        self.options = {
            'min_pyver': (2, 5),
            'max_pyver': (4, 0),
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
        return self._file_type('.args')

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

    def shortDescription(self):
        return self._test_file.base

    def _produces_output(self):
        return True

    def _get_expected(self):
        with open(self._test_file.source) as fobj:
            expected = get_expected_messages(fobj)

        lines = []
        if self._produces_output() and expected:
            with open(self._test_file.expected_output, 'U') as fobj:
                used = True
                for line in fobj:
                    parts = line.split(':', 2)
                    if len(parts) != 3 and used:
                        lines.append(line)
                    else:
                        linenum = int(parts[1])
                        if (linenum, parts[0]) in expected:
                            used = True
                            lines.append(line)
                        else:
                            used = False
        return expected, ''.join(lines)

    def _get_received(self):
        messages = self._linter.reporter.messages
        messages.sort(key=lambda m: (m.line, m.C, m.msg))
        text_result = cStringIO.StringIO()
        received = {}
        for msg in messages:
            received.setdefault((msg.line, msg.symbol), 0)
            received[msg.line, msg.symbol] += 1
            text_result.write(msg.format('{symbol}:{line}:{obj}:{msg}'))
            text_result.write('\n')
        return received, text_result.getvalue()

    def runTest(self):
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

    def _check_output_text(self, expected_messages, expected_text, received_text):
        self.assertMultiLineEqual(expected_text, received_text)


class LintModuleOutputUpdate(LintModuleTest):
    def _produces_output(self):
        return False

    def _check_output_text(self, expected_messages, expected_text, received_text):
        if expected_messages:
            with open(self._test_file.expected_output, 'w') as fobj:
                fobj.write(received_text)


def active_in_running_python_version(options):
    return options['min_pyver'] < sys.version_info <= options['max_pyver']


def suite():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'functional')
    suite = testlib.TestSuite()
    for fname in os.listdir(input_dir):
        if fname != '__init__.py' and fname.endswith('.py'):
            test_file = TestFile(input_dir, fname)
            if active_in_running_python_version(test_file.options):
                if UPDATE:
                    suite.addTest(LintModuleOutputUpdate(test_file))
                else:
                    suite.addTest(LintModuleTest(test_file))
    return suite


# TODO(tmarek): Port exhaustivity test from test_func once all tests have been added.


if __name__=='__main__':
    if '-u' in sys.argv:
        UPDATE = True
        sys.argv.remove('-u')
    testlib.unittest_main(defaultTest='suite')
