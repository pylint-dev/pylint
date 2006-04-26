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
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
""" Copyright (c) 2003-2005 LOGILAB S.A. (Paris, FRANCE).
 http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

__revision__ = '$Id: unittest_lint.py,v 1.16 2006-04-19 09:17:40 syt Exp $'

import unittest
import sys
import os
import tempfile
from os.path import join
from cStringIO import StringIO

from pylint.config import get_note_message
from pylint.lint import PyLinter, Run, sort_checkers, UnknownMessage
from pylint.utils import sort_msgs
from pylint import checkers

class SortMessagesTC(unittest.TestCase):
    
    def test(self):
        l = ['E0501', 'E0503', 'F0002', 'I0201', 'W0540',
             'R0202', 'F0203', 'R0220', 'W0321', 'I0001']
        self.assertEquals(sort_msgs(l), ['I0001', 'I0201',
                                         'R0202', 'R0220',
                                         'W0321', 'W0540',
                                         'E0501', 'E0503',
                                         'F0002', 'F0203'])

try:
    optimized = True
    raise AssertionError
except AssertionError:
    optimized = False
    
class GetNoteMessageTC(unittest.TestCase):
    def test(self):
        msg = None
        for note in range(-1, 11):
            note_msg = get_note_message(note)
            self.assertNotEquals(msg, note_msg)
            msg = note_msg
        if optimized:
            self.assertRaises(AssertionError, get_note_message, 11)
            
class RunTC(unittest.TestCase):

    def _test_run(self, args, exit_code=1, no_exit_fail=True):
        sys.stdout = StringIO()
        sys.sterr = StringIO()
        try:
            try:
                Run(args, quiet=1)
            except SystemExit, ex:
                self.assertEquals(ex.code, exit_code)
            else:
                if no_exit_fail:
                    self.fail()
        finally:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
        
    def test_no_args(self):
        self._test_run([], 1)
        
    def test_no_ext_file(self):
        self._test_run([join('input', 'noext')], no_exit_fail=False)

        
class PyLinterTC(unittest.TestCase):
    
    def setUp(self):
        self.linter = PyLinter()
        self.linter.disable_message_category('I')
        self.linter.config.persistent = 0
        # register checkers
        checkers.initialize(self.linter)
        
    def test_disable_all(self):
        self.linter.disable_all_checkers()
        checkers = sort_checkers(self.linter._checkers, enabled_only=0)
        self.assert_(len(checkers) > 1)
        checkers = sort_checkers(self.linter._checkers, enabled_only=1)
        self.assertEquals(checkers, [self.linter])
        
    def test_message_help(self):
        msg = self.linter.get_message_help('F0001')
        expected = 'F0001:\n  Used when an error occured preventing the analyzing of a module (unable to\n  find it for instance). This message belongs to the master checker.'
        self.assertEquals(' '.join(msg.splitlines()), ' '.join(expected.splitlines()))
        self.assertRaises(UnknownMessage, self.linter.get_message_help, 'YB12')
        
    def test_enable_message(self):
        linter = self.linter
        linter.open()
        linter.set_current_module('toto')
        self.assert_(linter.is_message_enabled('W0101'))
        self.assert_(linter.is_message_enabled('W0102'))
        linter.disable_message('W0101', scope='package')
        linter.disable_message('W0102', scope='module', line=1)
        self.assert_(not linter.is_message_enabled('W0101'))
        self.assert_(not linter.is_message_enabled('W0102', 1))
        linter.set_current_module('tutu')
        self.assert_(not linter.is_message_enabled('W0101'))
        self.assert_(linter.is_message_enabled('W0102'))        
        linter.enable_message('W0101', scope='package')
        linter.enable_message('W0102', scope='module', line=1)
        self.assert_(linter.is_message_enabled('W0101'))
        self.assert_(linter.is_message_enabled('W0102', 1))

    def test_enable_message_category(self):
        linter = self.linter
        linter.open()
        linter.set_current_module('toto')
        self.assert_(linter.is_message_enabled('W0101'))
        self.assert_(linter.is_message_enabled('R0102'))
        linter.disable_message_category('W', scope='package')
        linter.disable_message_category('REFACTOR', scope='module')
        self.assert_(not linter.is_message_enabled('W0101'))
        self.assert_(not linter.is_message_enabled('R0102'))
        linter.set_current_module('tutu')
        self.assert_(not linter.is_message_enabled('W0101'))
        self.assert_(linter.is_message_enabled('R0102'))        
        linter.enable_message_category('WARNING', scope='package')
        linter.enable_message_category('R', scope='module')
        self.assert_(linter.is_message_enabled('W0101'))
        self.assert_(linter.is_message_enabled('R0102'))

    def test_enable_message_block(self):
        linter = self.linter
        linter.open()
        filepath = join('input', 'func_block_disable_msg.py')
        linter.set_current_module('func_block_disable_msg')
        linter.process_module(open(filepath))
        orig_state = linter._module_msgs_state.copy()
        linter._module_msgs_state = {}
        linter.collect_block_lines(linter.get_astng(filepath, 'func_block_disable_msg'), orig_state)
        # global (module level)
        self.assert_(linter.is_message_enabled('W0613'))
        self.assert_(linter.is_message_enabled('E1101'))
        # meth1
        self.assert_(linter.is_message_enabled('W0613', 13))
        # meth2
        self.assert_(not linter.is_message_enabled('W0613', 18))
        # meth3
        self.assert_(not linter.is_message_enabled('E1101', 24))
        self.assert_(linter.is_message_enabled('E1101', 26))
        # meth4        
        self.assert_(not linter.is_message_enabled('E1101', 32))
        self.assert_(linter.is_message_enabled('E1101', 36))
        # meth5
        self.assert_(not linter.is_message_enabled('E1101', 42))
        self.assert_(not linter.is_message_enabled('E1101', 43))
        self.assert_(linter.is_message_enabled('E1101', 46))
        self.assert_(not linter.is_message_enabled('E1101', 49))
        self.assert_(not linter.is_message_enabled('E1101', 51))
        # meth6
        self.assert_(not linter.is_message_enabled('E1101', 57))
        self.assert_(linter.is_message_enabled('E1101', 61))
        self.assert_(not linter.is_message_enabled('E1101', 64))
        self.assert_(not linter.is_message_enabled('E1101', 66))
        
        self.assert_(linter.is_message_enabled('E0602', 57))
        self.assert_(linter.is_message_enabled('E0602', 61))
        self.assert_(not linter.is_message_enabled('E0602', 62))
        self.assert_(linter.is_message_enabled('E0602', 64))
        self.assert_(linter.is_message_enabled('E0602', 66))
        # meth7
        self.assert_(not linter.is_message_enabled('E1101', 70))
        self.assert_(linter.is_message_enabled('E1101', 72))
        self.assert_(linter.is_message_enabled('E1101', 75))
        self.assert_(linter.is_message_enabled('E1101', 77))
        
    def test_list_messages(self):
        sys.stdout = StringIO()
        try:
            # just invoke it, don't check the output
            self.linter.list_messages()
        finally:
            sys.stdout = sys.__stdout__

    def test_lint_ext_module_with_file_output(self):
        self.linter.config.files_output = True
        try:
            self.linter.check('StringIO')
            self.assert_(os.path.exists('pylint_StringIO.txt'))
            self.assert_(os.path.exists('pylint_global.txt'))
        finally:
            try:
                os.remove('pylint_StringIO.txt')
                os.remove('pylint_global.txt')
            except:
                pass

    def test_enable_report(self):
        self.assertEquals(self.linter.is_report_enabled('R0001'), True)
        self.linter.disable_report('R0001')
        self.assertEquals(self.linter.is_report_enabled('R0001'), False)
        self.linter.enable_report('R0001')
        self.assertEquals(self.linter.is_report_enabled('R0001'), True)

    def test_set_option_1(self):
        linter = self.linter
        linter.set_option('disable-msg', 'C0111,W0142')
        self.assert_(not linter.is_message_enabled('C0111'))
        self.assert_(not linter.is_message_enabled('W0142'))
        self.assert_(linter.is_message_enabled('W0113'))

    def test_set_option_2(self):
        linter = self.linter
        linter.set_option('disable-msg', ('C0111', 'W0142') )
        self.assert_(not linter.is_message_enabled('C0111'))
        self.assert_(not linter.is_message_enabled('W0142'))
        self.assert_(linter.is_message_enabled('W0113'))


from pylint import config

class ConfigTC(unittest.TestCase):

    def test_pylint_home(self):
        uhome = os.path.expanduser('~')
        if uhome == '~':
            expected = '.pylint.d'
        else:
            expected = os.path.join(uhome, '.pylint.d')
        self.assertEquals(config.PYLINT_HOME, expected)

        try:
            pylintd = join(tempfile.gettempdir(), '.pylint.d')
            os.environ['PYLINTHOME'] = pylintd
            try:
                reload(config)
                self.assertEquals(config.PYLINT_HOME, pylintd)
            finally:
                try:
                    os.remove(pylintd)
                except:
                    pass
        finally:
            del os.environ['PYLINTHOME']
        
    def test_pylintrc(self):
        try:
            self.assertEquals(config.PYLINTRC, None)
            os.environ['PYLINTRC'] = join(tempfile.gettempdir(), '.pylintrc')
            reload(config)
            self.assertEquals(config.PYLINTRC, None)
            os.environ['PYLINTRC'] = '.'
            reload(config)
            self.assertEquals(config.PYLINTRC, None)
        finally:
            del os.environ['PYLINTRC']
            reload(config)
        
if __name__ == '__main__':
    unittest.main()
