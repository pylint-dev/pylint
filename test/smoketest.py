# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import sys
from os.path import join, dirname, abspath
from cStringIO import StringIO

from logilab.common.testlib import TestCase, unittest_main, tag

from pylint.lint import Run
from pylint.reporters.text import *
from pylint.reporters.html import HTMLReporter

HERE = abspath(dirname(__file__))

class RunTC(TestCase):

    def _runtest(self, args, reporter=None, code=28):
        if sys.version_info < (2, 5) and 'pylint.lint' in args:
            code = 30
        try:
            sys.stderr = sys.stdout = stream = StringIO()
            try:
                Run(args, reporter=reporter)
            except SystemExit, ex:
                self.assertEquals(ex.code, code)
            else:
                self.fail('expected system exit')
        finally:
            sys.stderr = sys.__stderr__
            sys.stdout = sys.__stdout__
            
    @tag('smoke')
    def test0(self):
        """make pylint checking itself"""
        self._runtest(['pylint.__pkginfo__'], reporter=TextReporter(StringIO()),
                      code=0)
        
    @tag('smoke')
    def test1(self):
        """make pylint checking itself"""
        self._runtest(['--include-ids=y', 'pylint.lint'], reporter=TextReporter(StringIO()))
    
    @tag('smoke')
    def test2(self):
        """make pylint checking itself"""
        self._runtest(['pylint.lint'], reporter=ParseableTextReporter(StringIO()))
    
    @tag('smoke')
    def test3(self):
        """make pylint checking itself"""
        self._runtest(['pylint.lint'], reporter=HTMLReporter(StringIO()))
    
    @tag('smoke')
    def test4(self):
        """make pylint checking itself"""
        self._runtest(['pylint.lint'], reporter=ColorizedTextReporter(StringIO()))
    
    @tag('smoke')
    def test5(self):
        """make pylint checking itself"""
        self._runtest(['pylint.lint'], reporter=VSTextReporter(StringIO()))
        
    @tag('smoke')
    def test_no_ext_file(self):
        self._runtest([join(HERE, 'input', 'noext')], code=0)
        
    @tag('smoke')
    def test_w0704_ignored(self):
        self._runtest([join(HERE, 'input', 'ignore_except_pass_by_default.py')], code=0)
    
    @tag('smoke', 'help', 'config')
    def test_generate_config_option(self):
        """make pylint checking itself"""
        self._runtest(['--generate-rcfile'], reporter=HTMLReporter(StringIO()),
                      code=0)
    
    @tag('smoke', 'help')
    def test_help_message_option(self):
        """make pylint checking itself"""
        self._runtest(['--help-msg', 'W0101'], reporter=HTMLReporter(StringIO()),
                      code=0)
        
    @tag('smoke', 'help')
    def test_error_help_message_option(self):
        self._runtest(['--help-msg', 'WX101'], reporter=HTMLReporter(StringIO()),
                      code=0)
        
    @tag('smoke', 'usage')
    def test_error_missing_arguments(self):
        self._runtest([], reporter=HTMLReporter(StringIO()),
                      code=32)
    
        
if __name__ == '__main__':
    unittest_main()
