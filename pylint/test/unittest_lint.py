# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from contextlib import contextmanager
import sys
import os
import tempfile
from shutil import rmtree
from os import getcwd, chdir
from os.path import join, basename, dirname, isdir, abspath, sep
import unittest

import six
from six.moves import reload_module

from pylint import config, lint
from pylint.lint import PyLinter, Run, preprocess_options, \
     ArgumentPreprocessingError
from pylint.utils import MSG_STATE_SCOPE_CONFIG, MSG_STATE_SCOPE_MODULE, MSG_STATE_CONFIDENCE, \
    MessagesStore, PyLintASTWalker, MessageDefinition, FileState, \
    build_message_def, tokenize_module, UnknownMessage
from pylint.testutils import TestReporter, catch_warnings
from pylint.reporters import text, html
from pylint import checkers
from pylint.checkers.utils import check_messages
from pylint import interfaces

if os.name == 'java':
    if os._name == 'nt':
        HOME = 'USERPROFILE'
    else:
        HOME = 'HOME'
else:
    if sys.platform == 'win32':
        HOME = 'USERPROFILE'
    else:
        HOME = 'HOME'

@contextmanager
def fake_home():
    folder = tempfile.mkdtemp('fake-home')
    old_home = os.environ.get(HOME)
    try:
        os.environ[HOME] = folder
        yield
    finally:
        os.environ.pop('PYLINTRC', '')
        if old_home is None:
            del os.environ[HOME]
        else:
            os.environ[HOME] = old_home
        rmtree(folder, ignore_errors=True)

def remove(file):
    try:
        os.remove(file)
    except OSError:
        pass

HERE = abspath(dirname(__file__))
INPUTDIR = join(HERE, 'input')


@contextmanager
def tempdir():
    """Create a temp directory and change the current location to it.

    This is supposed to be used with a *with* statement.
    """
    tmp = tempfile.mkdtemp()

    # Get real path of tempfile, otherwise test fail on mac os x
    current_dir = getcwd()
    chdir(tmp)
    abs_tmp = abspath('.')

    try:
        yield abs_tmp
    finally:
        chdir(current_dir)
        rmtree(abs_tmp)


def create_files(paths, chroot='.'):
    """Creates directories and files found in <path>.

    :param paths: list of relative paths to files or directories
    :param chroot: the root directory in which paths will be created

    >>> from os.path import isdir, isfile
    >>> isdir('/tmp/a')
    False
    >>> create_files(['a/b/foo.py', 'a/b/c/', 'a/b/c/d/e.py'], '/tmp')
    >>> isdir('/tmp/a')
    True
    >>> isdir('/tmp/a/b/c')
    True
    >>> isfile('/tmp/a/b/c/d/e.py')
    True
    >>> isfile('/tmp/a/b/foo.py')
    True
    """
    dirs, files = set(), set()
    for path in paths:
        path = join(chroot, path)
        filename = basename(path)
        # path is a directory path
        if filename == '':
            dirs.add(path)
        # path is a filename path
        else:
            dirs.add(dirname(path))
            files.add(path)
    for dirpath in dirs:
        if not isdir(dirpath):
            os.makedirs(dirpath)
    for filepath in files:
        open(filepath, 'w').close()


class SysPathFixupTC(unittest.TestCase):
    def setUp(self):
        self.orig = list(sys.path)
        self.fake = [1, 2, 3]
        sys.path[:] = self.fake

    def tearDown(self):
        sys.path[:] = self.orig

    def test_no_args(self):
        with lint.fix_import_path([]):
            self.assertEqual(sys.path, self.fake)
        self.assertEqual(sys.path, self.fake)

    def test_one_arg(self):
        with tempdir() as chroot:
            create_files(['a/b/__init__.py'])
            expected = [join(chroot, 'a')] + self.fake

            cases = (
                ['a/b/'],
                ['a/b'],
                ['a/b/__init__.py'],
                ['a/'],
                ['a'],
            )

            self.assertEqual(sys.path, self.fake)
            for case in cases:
                with lint.fix_import_path(case):
                    self.assertEqual(sys.path, expected)
                self.assertEqual(sys.path, self.fake)

    def test_two_similar_args(self):
        with tempdir() as chroot:
            create_files(['a/b/__init__.py', 'a/c/__init__.py'])
            expected = [join(chroot, 'a')] + self.fake

            cases = (
                ['a/b', 'a/c'],
                ['a/c/', 'a/b/'],
                ['a/b/__init__.py', 'a/c/__init__.py'],
                ['a', 'a/c/__init__.py'],
            )

            self.assertEqual(sys.path, self.fake)
            for case in cases:
                with lint.fix_import_path(case):
                    self.assertEqual(sys.path, expected)
                self.assertEqual(sys.path, self.fake)

    def test_more_args(self):
        with tempdir() as chroot:
            create_files(['a/b/c/__init__.py', 'a/d/__init__.py', 'a/e/f.py'])
            expected = [
                join(chroot, suffix)
                for suffix in [sep.join(('a', 'b')), 'a', sep.join(('a', 'e'))]
            ] + self.fake

            cases = (
                ['a/b/c/__init__.py', 'a/d/__init__.py', 'a/e/f.py'],
                ['a/b/c', 'a', 'a/e'],
                ['a/b/c', 'a', 'a/b/c', 'a/e', 'a'],
            )

            self.assertEqual(sys.path, self.fake)
            for case in cases:
                with lint.fix_import_path(case):
                    self.assertEqual(sys.path, expected)
                self.assertEqual(sys.path, self.fake)


class PyLinterTC(unittest.TestCase):

    def setUp(self):
        self.linter = PyLinter()
        self.linter.disable('I')
        self.linter.config.persistent = 0
        # register checkers
        checkers.initialize(self.linter)
        self.linter.set_reporter(TestReporter())

    def init_linter(self):
        linter = self.linter
        linter.open()
        linter.set_current_module('toto')
        linter.file_state = FileState('toto')
        return linter

    def test_pylint_visit_method_taken_in_account(self):
        class CustomChecker(checkers.BaseChecker):
            __implements__ = interfaces.IAstroidChecker
            name = 'custom'
            msgs = {'W9999': ('', 'custom', '')}

            @check_messages('custom')
            def visit_class(self, _):
               pass

        self.linter.register_checker(CustomChecker(self.linter))
        self.linter.open()
        out = six.moves.StringIO()
        self.linter.set_reporter(text.TextReporter(out))
        self.linter.check('abc')

    def test_enable_message(self):
        linter = self.init_linter()
        self.assertTrue(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('W0102'))
        linter.disable('W0101', scope='package')
        linter.disable('W0102', scope='module', line=1)
        self.assertFalse(linter.is_message_enabled('W0101'))
        self.assertFalse(linter.is_message_enabled('W0102', 1))
        linter.set_current_module('tutu')
        self.assertFalse(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('W0102'))
        linter.enable('W0101', scope='package')
        linter.enable('W0102', scope='module', line=1)
        self.assertTrue(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('W0102', 1))

    def test_enable_message_category(self):
        linter = self.init_linter()
        self.assertTrue(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('C0202'))
        linter.disable('W', scope='package')
        linter.disable('C', scope='module', line=1)
        self.assertFalse(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('C0202'))
        self.assertFalse(linter.is_message_enabled('C0202', line=1))
        linter.set_current_module('tutu')
        self.assertFalse(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('C0202'))
        linter.enable('W', scope='package')
        linter.enable('C', scope='module', line=1)
        self.assertTrue(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('C0202'))
        self.assertTrue(linter.is_message_enabled('C0202', line=1))

    def test_message_state_scope(self):
        class FakeConfig(object):
            confidence = ['HIGH']

        linter = self.init_linter()
        linter.disable('C0202')
        self.assertEqual(MSG_STATE_SCOPE_CONFIG,
                         linter.get_message_state_scope('C0202'))
        linter.disable('W0101', scope='module', line=3)
        self.assertEqual(MSG_STATE_SCOPE_CONFIG,
                         linter.get_message_state_scope('C0202'))
        self.assertEqual(MSG_STATE_SCOPE_MODULE,
                         linter.get_message_state_scope('W0101', 3))
        linter.enable('W0102', scope='module', line=3)
        self.assertEqual(MSG_STATE_SCOPE_MODULE,
                         linter.get_message_state_scope('W0102', 3))
        linter.config = FakeConfig()
        self.assertEqual(
            MSG_STATE_CONFIDENCE,
            linter.get_message_state_scope('this-is-bad',
                                           confidence=interfaces.INFERENCE))

    def test_enable_message_block(self):
        linter = self.init_linter()
        linter.open()
        filepath = join(INPUTDIR, 'func_block_disable_msg.py')
        linter.set_current_module('func_block_disable_msg')
        astroid = linter.get_ast(filepath, 'func_block_disable_msg')
        linter.process_tokens(tokenize_module(astroid))
        fs = linter.file_state
        fs.collect_block_lines(linter.msgs_store, astroid)
        # global (module level)
        self.assertTrue(linter.is_message_enabled('W0613'))
        self.assertTrue(linter.is_message_enabled('E1101'))
        # meth1
        self.assertTrue(linter.is_message_enabled('W0613', 13))
        # meth2
        self.assertFalse(linter.is_message_enabled('W0613', 18))
        # meth3
        self.assertFalse(linter.is_message_enabled('E1101', 24))
        self.assertTrue(linter.is_message_enabled('E1101', 26))
        # meth4
        self.assertFalse(linter.is_message_enabled('E1101', 32))
        self.assertTrue(linter.is_message_enabled('E1101', 36))
        # meth5
        self.assertFalse(linter.is_message_enabled('E1101', 42))
        self.assertFalse(linter.is_message_enabled('E1101', 43))
        self.assertTrue(linter.is_message_enabled('E1101', 46))
        self.assertFalse(linter.is_message_enabled('E1101', 49))
        self.assertFalse(linter.is_message_enabled('E1101', 51))
        # meth6
        self.assertFalse(linter.is_message_enabled('E1101', 57))
        self.assertTrue(linter.is_message_enabled('E1101', 61))
        self.assertFalse(linter.is_message_enabled('E1101', 64))
        self.assertFalse(linter.is_message_enabled('E1101', 66))

        self.assertTrue(linter.is_message_enabled('E0602', 57))
        self.assertTrue(linter.is_message_enabled('E0602', 61))
        self.assertFalse(linter.is_message_enabled('E0602', 62))
        self.assertTrue(linter.is_message_enabled('E0602', 64))
        self.assertTrue(linter.is_message_enabled('E0602', 66))
        # meth7
        self.assertFalse(linter.is_message_enabled('E1101', 70))
        self.assertTrue(linter.is_message_enabled('E1101', 72))
        self.assertTrue(linter.is_message_enabled('E1101', 75))
        self.assertTrue(linter.is_message_enabled('E1101', 77))

        fs = linter.file_state
        self.assertEqual(17, fs._suppression_mapping['W0613', 18])
        self.assertEqual(30, fs._suppression_mapping['E1101', 33])
        self.assertTrue(('E1101', 46) not in fs._suppression_mapping)
        self.assertEqual(1, fs._suppression_mapping['C0302', 18])
        self.assertEqual(1, fs._suppression_mapping['C0302', 50])
        # This is tricky. While the disable in line 106 is disabling
        # both 108 and 110, this is usually not what the user wanted.
        # Therefore, we report the closest previous disable comment.
        self.assertEqual(106, fs._suppression_mapping['E1101', 108])
        self.assertEqual(109, fs._suppression_mapping['E1101', 110])

    def test_enable_by_symbol(self):
        """messages can be controlled by symbolic names.

        The state is consistent across symbols and numbers.
        """
        linter = self.init_linter()
        self.assertTrue(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('unreachable'))
        self.assertTrue(linter.is_message_enabled('W0102'))
        self.assertTrue(linter.is_message_enabled('dangerous-default-value'))
        linter.disable('unreachable', scope='package')
        linter.disable('dangerous-default-value', scope='module', line=1)
        self.assertFalse(linter.is_message_enabled('W0101'))
        self.assertFalse(linter.is_message_enabled('unreachable'))
        self.assertFalse(linter.is_message_enabled('W0102', 1))
        self.assertFalse(linter.is_message_enabled('dangerous-default-value', 1))
        linter.set_current_module('tutu')
        self.assertFalse(linter.is_message_enabled('W0101'))
        self.assertFalse(linter.is_message_enabled('unreachable'))
        self.assertTrue(linter.is_message_enabled('W0102'))
        self.assertTrue(linter.is_message_enabled('dangerous-default-value'))
        linter.enable('unreachable', scope='package')
        linter.enable('dangerous-default-value', scope='module', line=1)
        self.assertTrue(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('unreachable'))
        self.assertTrue(linter.is_message_enabled('W0102', 1))
        self.assertTrue(linter.is_message_enabled('dangerous-default-value', 1))

    def test_lint_ext_module_with_file_output(self):
        self.linter.set_reporter(text.TextReporter())
        if sys.version_info < (3, 0):
            strio = 'StringIO'
        else:
            strio = 'io'
        self.linter.config.files_output = True
        pylint_strio = 'pylint_%s.txt' % strio
        files = [pylint_strio, 'pylint_global.txt']
        for file in files:
            self.addCleanup(remove, file)

        self.linter.check(strio)
        self.linter.generate_reports()
        for f in files:
            self.assertTrue(os.path.exists(f))

    def test_enable_report(self):
        self.assertEqual(self.linter.report_is_enabled('RP0001'), True)
        self.linter.disable('RP0001')
        self.assertEqual(self.linter.report_is_enabled('RP0001'), False)
        self.linter.enable('RP0001')
        self.assertEqual(self.linter.report_is_enabled('RP0001'), True)

    def test_report_output_format_aliased(self):
        text.register(self.linter)
        self.linter.set_option('output-format', 'text')
        self.assertEqual(self.linter.reporter.__class__.__name__, 'TextReporter')

    def test_report_output_format_custom(self):
        this_module = sys.modules[__name__]
        class TestReporter(object):
            pass
        this_module.TestReporter = TestReporter
        class_name = ".".join((this_module.__name__, 'TestReporter'))
        self.linter.set_option('output-format', class_name)
        self.assertEqual(self.linter.reporter.__class__.__name__, 'TestReporter')

    def test_set_option_1(self):
        linter = self.linter
        linter.set_option('disable', 'C0111,W0234')
        self.assertFalse(linter.is_message_enabled('C0111'))
        self.assertFalse(linter.is_message_enabled('W0234'))
        self.assertTrue(linter.is_message_enabled('W0113'))
        self.assertFalse(linter.is_message_enabled('missing-docstring'))
        self.assertFalse(linter.is_message_enabled('non-iterator-returned'))

    def test_set_option_2(self):
        linter = self.linter
        linter.set_option('disable', ('C0111', 'W0234') )
        self.assertFalse(linter.is_message_enabled('C0111'))
        self.assertFalse(linter.is_message_enabled('W0234'))
        self.assertTrue(linter.is_message_enabled('W0113'))
        self.assertFalse(linter.is_message_enabled('missing-docstring'))
        self.assertFalse(linter.is_message_enabled('non-iterator-returned'))

    def test_enable_checkers(self):
        self.linter.disable('design')
        self.assertFalse('design' in [c.name for c in self.linter.prepare_checkers()])
        self.linter.enable('design')
        self.assertTrue('design' in [c.name for c in self.linter.prepare_checkers()])

    def test_errors_only(self):
        linter = self.linter
        self.linter.error_mode()
        checkers = self.linter.prepare_checkers()
        checker_names = set(c.name for c in checkers)
        should_not = set(('design', 'format', 'metrics',
                      'miscellaneous', 'similarities'))
        self.assertSetEqual(set(), should_not & checker_names)

    def test_disable_similar(self):
        self.linter.set_option('disable', 'RP0801')
        self.linter.set_option('disable', 'R0801')
        self.assertFalse('similarities' in [c.name for c in self.linter.prepare_checkers()])

    def test_disable_alot(self):
        """check that we disabled a lot of checkers"""
        self.linter.set_option('reports', False)
        self.linter.set_option('disable', 'R,C,W')
        checker_names = [c.name for c in self.linter.prepare_checkers()]
        for cname in  ('design', 'metrics', 'similarities'):
            self.assertFalse(cname in checker_names, cname)

    def test_addmessage(self):
        self.linter.set_reporter(TestReporter())
        self.linter.open()
        self.linter.set_current_module('0123')
        self.linter.add_message('C0301', line=1, args=(1, 2))
        self.linter.add_message('line-too-long', line=2, args=(3, 4))
        self.assertEqual(
            ['C:  1: Line too long (1/2)', 'C:  2: Line too long (3/4)'],
            self.linter.reporter.messages)

    def test_init_hooks_called_before_load_plugins(self):
        self.assertRaises(RuntimeError,
                          Run, ['--load-plugins', 'unexistant', '--init-hook', 'raise RuntimeError'])
        self.assertRaises(RuntimeError,
                          Run, ['--init-hook', 'raise RuntimeError', '--load-plugins', 'unexistant'])


    def test_analyze_explicit_script(self):
        self.linter.set_reporter(TestReporter())
        self.linter.check(os.path.join(os.path.dirname(__file__), 'data', 'ascript'))
        self.assertEqual(
            ['C:  2: Line too long (175/100)'],
            self.linter.reporter.messages)

    def test_html_reporter_missing_files(self):
        output = six.StringIO()
        with catch_warnings():
            self.linter.set_reporter(html.HTMLReporter(output))

        self.linter.set_option('output-format', 'html')
        self.linter.check('troppoptop.py')
        self.linter.generate_reports()
        value = output.getvalue()
        self.assertIn('troppoptop.py', value)
        self.assertIn('fatal', value)

    def test_python3_checker_disabled(self):
        checker_names = [c.name for c in self.linter.prepare_checkers()]
        self.assertNotIn('python3', checker_names)

        self.linter.set_option('enable', 'python3')
        checker_names = [c.name for c in self.linter.prepare_checkers()]
        self.assertIn('python3', checker_names)


class ConfigTC(unittest.TestCase):

    def setUp(self):
        os.environ.pop('PYLINTRC', None)

    def test_pylint_home(self):
        uhome = os.path.expanduser('~')
        if uhome == '~':
            expected = '.pylint.d'
        else:
            expected = os.path.join(uhome, '.pylint.d')
        self.assertEqual(config.PYLINT_HOME, expected)

        try:
            pylintd = join(tempfile.gettempdir(), '.pylint.d')
            os.environ['PYLINTHOME'] = pylintd
            try:
                reload_module(config)
                self.assertEqual(config.PYLINT_HOME, pylintd)
            finally:
                try:
                    os.remove(pylintd)
                except:
                    pass
        finally:
            del os.environ['PYLINTHOME']

    def test_pylintrc(self):
        with fake_home():
            try:
                self.assertEqual(config.find_pylintrc(), None)
                os.environ['PYLINTRC'] = join(tempfile.gettempdir(),
                                              '.pylintrc')
                self.assertEqual(config.find_pylintrc(), None)
                os.environ['PYLINTRC'] = '.'
                self.assertEqual(config.find_pylintrc(), None)
            finally:
                reload_module(config)

    def test_pylintrc_parentdir(self):
        with tempdir() as chroot:

            create_files(['a/pylintrc', 'a/b/__init__.py', 'a/b/pylintrc',
                          'a/b/c/__init__.py', 'a/b/c/d/__init__.py',
                          'a/b/c/d/e/.pylintrc'])
            with fake_home():
                self.assertEqual(config.find_pylintrc(), None)
            results = {'a'       : join(chroot, 'a', 'pylintrc'),
                       'a/b'     : join(chroot, 'a', 'b', 'pylintrc'),
                       'a/b/c'   : join(chroot, 'a', 'b', 'pylintrc'),
                       'a/b/c/d' : join(chroot, 'a', 'b', 'pylintrc'),
                       'a/b/c/d/e' : join(chroot, 'a', 'b', 'c', 'd', 'e', '.pylintrc'),
                       }
            for basedir, expected in results.items():
                os.chdir(join(chroot, basedir))
                self.assertEqual(config.find_pylintrc(), expected)

    def test_pylintrc_parentdir_no_package(self):
        with tempdir() as chroot:
            with fake_home():
                create_files(['a/pylintrc', 'a/b/pylintrc', 'a/b/c/d/__init__.py'])
                self.assertEqual(config.find_pylintrc(), None)
                results = {'a'       : join(chroot, 'a', 'pylintrc'),
                           'a/b'     : join(chroot, 'a', 'b', 'pylintrc'),
                           'a/b/c'   : None,
                           'a/b/c/d' : None,
                           }
                for basedir, expected in results.items():
                    os.chdir(join(chroot, basedir))
                    self.assertEqual(config.find_pylintrc(), expected)


class PreprocessOptionsTC(unittest.TestCase):
    def _callback(self, name, value):
        self.args.append((name, value))

    def test_value_equal(self):
        self.args = []
        preprocess_options(['--foo', '--bar=baz', '--qu=ux'],
                           {'foo' : (self._callback, False),
                            'qu' : (self._callback, True)})
        self.assertEqual(
            [('foo', None), ('qu', 'ux')], self.args)

    def test_value_space(self):
        self.args = []
        preprocess_options(['--qu', 'ux'],
                           {'qu' : (self._callback, True)})
        self.assertEqual(
            [('qu', 'ux')], self.args)

    def test_error_missing_expected_value(self):
        self.assertRaises(
            ArgumentPreprocessingError,
            preprocess_options,
            ['--foo', '--bar', '--qu=ux'],
            {'bar' : (None, True)})
        self.assertRaises(
            ArgumentPreprocessingError,
            preprocess_options,
            ['--foo', '--bar'],
            {'bar' : (None, True)})

    def test_error_unexpected_value(self):
        self.assertRaises(
            ArgumentPreprocessingError,
            preprocess_options,
            ['--foo', '--bar=spam', '--qu=ux'],
            {'bar' : (None, False)})


class MessagesStoreTC(unittest.TestCase):
    def setUp(self):
        self.store = MessagesStore()
        class Checker(object):
            name = 'achecker'
            msgs = {
                'W1234': ('message', 'msg-symbol', 'msg description.',
                          {'old_names': [('W0001', 'old-symbol')]}),
                'E1234': ('Duplicate keyword argument %r in %s call',
                          'duplicate-keyword-arg',
                          'Used when a function call passes the same keyword argument multiple times.',
                          {'maxversion': (2, 6)}),
                }
        self.store.register_messages(Checker())

    def _compare_messages(self, desc, msg, checkerref=False):
        self.assertMultiLineEqual(desc, msg.format_help(checkerref=checkerref))

    def test_check_message_id(self):
        self.assertIsInstance(self.store.check_message_id('W1234'),
                              MessageDefinition)
        self.assertRaises(UnknownMessage,
                          self.store.check_message_id, 'YB12')

    def test_message_help(self):
        msg = self.store.check_message_id('W1234')
        self._compare_messages(
            ''':msg-symbol (W1234): *message*
  msg description. This message belongs to the achecker checker.''',
            msg, checkerref=True)
        self._compare_messages(
            ''':msg-symbol (W1234): *message*
  msg description.''',
            msg, checkerref=False)

    def test_message_help_minmax(self):
        # build the message manually to be python version independant
        msg = self.store.check_message_id('E1234')
        self._compare_messages(
            ''':duplicate-keyword-arg (E1234): *Duplicate keyword argument %r in %s call*
  Used when a function call passes the same keyword argument multiple times.
  This message belongs to the achecker checker. It can't be emitted when using
  Python >= 2.6.''',
            msg, checkerref=True)
        self._compare_messages(
            ''':duplicate-keyword-arg (E1234): *Duplicate keyword argument %r in %s call*
  Used when a function call passes the same keyword argument multiple times.
  This message can't be emitted when using Python >= 2.6.''',
            msg, checkerref=False)

    def test_list_messages(self):
        sys.stdout = six.StringIO()
        try:
            self.store.list_messages()
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        # cursory examination of the output: we're mostly testing it completes
        self.assertIn(':msg-symbol (W1234): *message*', output)

    def test_add_renamed_message(self):
        self.store.add_renamed_message('W1234', 'old-bad-name', 'msg-symbol')
        self.assertEqual('msg-symbol',
                         self.store.check_message_id('W1234').symbol)
        self.assertEqual('msg-symbol',
                         self.store.check_message_id('old-bad-name').symbol)

    def test_renamed_message_register(self):
        self.assertEqual('msg-symbol',
                         self.store.check_message_id('W0001').symbol)
        self.assertEqual('msg-symbol',
                         self.store.check_message_id('old-symbol').symbol)

   
if __name__ == '__main__':
    unittest.main()
