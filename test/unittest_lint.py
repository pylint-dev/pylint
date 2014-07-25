# Copyright (c) 2003-2014 LOGILAB S.A. (Paris, FRANCE).
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import sys
import os
import tempfile
from shutil import rmtree
from os import getcwd, chdir
from os.path import join, basename, dirname, isdir, abspath
from cStringIO import StringIO

from logilab.common.testlib import TestCase, unittest_main, create_files
from logilab.common.compat import reload

from pylint import config
from pylint.lint import PyLinter, Run, UnknownMessage, preprocess_options, \
     ArgumentPreprocessingError
from pylint.utils import MSG_STATE_SCOPE_CONFIG, MSG_STATE_SCOPE_MODULE, \
    MessagesStore, PyLintASTWalker, MessageDefinition, FileState, \
    build_message_def, tokenize_module
from pylint.testutils import TestReporter
from pylint.reporters import text
from pylint import checkers

if sys.platform == 'win32':
    HOME = 'USERPROFILE'
else:
    HOME = 'HOME'

class GetNoteMessageTC(TestCase):
    def test(self):
        msg = None
        for note in range(-1, 11):
            note_msg = config.get_note_message(note)
            self.assertNotEqual(msg, note_msg)
            msg = note_msg


HERE = abspath(dirname(__file__))
INPUTDIR = join(HERE, 'input')


class PyLinterTC(TestCase):

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
        self.assertTrue(linter.is_message_enabled('C0121'))
        linter.disable('W', scope='package')
        linter.disable('C', scope='module', line=1)
        self.assertFalse(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('C0121'))
        self.assertFalse(linter.is_message_enabled('C0121', line=1))
        linter.set_current_module('tutu')
        self.assertFalse(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('C0121'))
        linter.enable('W', scope='package')
        linter.enable('C', scope='module', line=1)
        self.assertTrue(linter.is_message_enabled('W0101'))
        self.assertTrue(linter.is_message_enabled('C0121'))
        self.assertTrue(linter.is_message_enabled('C0121', line=1))

    def test_message_state_scope(self):
        linter = self.init_linter()
        fs = linter.file_state
        linter.disable('C0121')
        self.assertEqual(MSG_STATE_SCOPE_CONFIG,
                         fs._message_state_scope('C0121'))
        linter.disable('W0101', scope='module', line=3)
        self.assertEqual(MSG_STATE_SCOPE_CONFIG,
                         fs._message_state_scope('C0121'))
        self.assertEqual(MSG_STATE_SCOPE_MODULE,
                         fs._message_state_scope('W0101', 3))
        linter.enable('W0102', scope='module', line=3)
        self.assertEqual(MSG_STATE_SCOPE_MODULE,
                         fs._message_state_scope('W0102', 3))

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
        try:
            self.linter.check(strio)
            self.assertTrue(os.path.exists(pylint_strio))
            self.assertTrue(os.path.exists('pylint_global.txt'))
        finally:
            try:
                os.remove(pylint_strio)
                os.remove('pylint_global.txt')
            except:
                pass

    def test_lint_should_analyze_file(self):
        self.linter.set_reporter(text.TextReporter())
        self.linter.config.files_output = True
        self.linter.should_analyze_file = lambda *args: False
        self.linter.check('logilab')
        self.assertTrue(os.path.exists('pylint_logilab.txt'))
        self.assertFalse(os.path.exists('pylint_logilab_common.txt'))

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
        linter.set_option('disable', 'C0111,W0142')
        self.assertFalse(linter.is_message_enabled('C0111'))
        self.assertFalse(linter.is_message_enabled('W0142'))
        self.assertTrue(linter.is_message_enabled('W0113'))
        self.assertFalse(linter.is_message_enabled('missing-docstring'))
        self.assertFalse(linter.is_message_enabled('star-args'))
        # no name for W0113

    def test_set_option_2(self):
        linter = self.linter
        linter.set_option('disable', ('C0111', 'W0142') )
        self.assertFalse(linter.is_message_enabled('C0111'))
        self.assertFalse(linter.is_message_enabled('W0142'))
        self.assertTrue(linter.is_message_enabled('W0113'))
        self.assertFalse(linter.is_message_enabled('missing-docstring'))
        self.assertFalse(linter.is_message_enabled('star-args'))
        # no name for W0113

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
        should_not = set(('design', 'format', 'imports', 'metrics',
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
        for cname in  ('design', 'metrics', 'similarities',
                       'imports'): # as a Fatal message that should be ignored
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
        self.linter.check(self.datapath('ascript'))
        self.assertEqual(
            ['C:  2: Line too long (175/80)'],
            self.linter.reporter.messages)


class ConfigTC(TestCase):

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
                reload(config)
                self.assertEqual(config.PYLINT_HOME, pylintd)
            finally:
                try:
                    os.remove(pylintd)
                except:
                    pass
        finally:
            del os.environ['PYLINTHOME']

    def test_pylintrc(self):
        fake_home = tempfile.mkdtemp('fake-home')
        home = os.environ[HOME]
        try:
            os.environ[HOME] = fake_home
            self.assertEqual(config.find_pylintrc(), None)
            os.environ['PYLINTRC'] = join(tempfile.gettempdir(), '.pylintrc')
            self.assertEqual(config.find_pylintrc(), None)
            os.environ['PYLINTRC'] = '.'
            self.assertEqual(config.find_pylintrc(), None)
        finally:
            os.environ.pop('PYLINTRC', '')
            os.environ[HOME] = home
            rmtree(fake_home, ignore_errors=True)
            reload(config)

    def test_pylintrc_parentdir(self):
        chroot = tempfile.mkdtemp()

        # Get real path of tempfile, otherwise test fail on mac os x
        cdir = getcwd()
        chdir(chroot)
        chroot = abspath('.')
        chdir(cdir)

        try:
            create_files(['a/pylintrc', 'a/b/__init__.py', 'a/b/pylintrc',
                          'a/b/c/__init__.py', 'a/b/c/d/__init__.py'], chroot)
            os.chdir(chroot)
            fake_home = tempfile.mkdtemp('fake-home')
            home = os.environ[HOME]
            try:
                os.environ[HOME] = fake_home
                self.assertEqual(config.find_pylintrc(), None)
            finally:
                os.environ[HOME] = home
                os.rmdir(fake_home)
            results = {'a'       : join(chroot, 'a', 'pylintrc'),
                       'a/b'     : join(chroot, 'a', 'b', 'pylintrc'),
                       'a/b/c'   : join(chroot, 'a', 'b', 'pylintrc'),
                       'a/b/c/d' : join(chroot, 'a', 'b', 'pylintrc'),
                       }
            for basedir, expected in results.items():
                os.chdir(join(chroot, basedir))
                self.assertEqual(config.find_pylintrc(), expected)
        finally:
            os.chdir(HERE)
            rmtree(chroot)

    def test_pylintrc_parentdir_no_package(self):
        chroot = tempfile.mkdtemp()

        # Get real path of tempfile, otherwise test fail on mac os x
        cdir = getcwd()
        chdir(chroot)
        chroot = abspath('.')
        chdir(cdir)

        fake_home = tempfile.mkdtemp('fake-home')
        home = os.environ[HOME]
        os.environ[HOME] = fake_home
        try:
            create_files(['a/pylintrc', 'a/b/pylintrc', 'a/b/c/d/__init__.py'], chroot)
            os.chdir(chroot)
            self.assertEqual(config.find_pylintrc(), None)
            results = {'a'       : join(chroot, 'a', 'pylintrc'),
                       'a/b'     : join(chroot, 'a', 'b', 'pylintrc'),
                       'a/b/c'   : None,
                       'a/b/c/d' : None,
                       }
            for basedir, expected in results.items():
                os.chdir(join(chroot, basedir))
                self.assertEqual(config.find_pylintrc(), expected)
        finally:
            os.environ[HOME] = home
            rmtree(fake_home, ignore_errors=True)
            os.chdir(HERE)
            rmtree(chroot)


class PreprocessOptionsTC(TestCase):
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


class MessagesStoreTC(TestCase):
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
        # replace \r\n with \n, because
        # logilab.common.textutils.normalize_text
        # uses os.linesep, which will
        # not properly compare with triple
        # quoted multilines used in these tests
        self.assertMultiLineEqual(
            desc,
            msg.format_help(checkerref=checkerref).replace('\r\n', '\n'))

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
        sys.stdout = StringIO()
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
    unittest_main()
