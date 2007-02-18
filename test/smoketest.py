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
from cStringIO import StringIO

from logilab.common.testlib import TestCase, unittest_main

from pylint.lint import Run
from pylint.reporters.text import *
from pylint.reporters.html import HTMLReporter

    
class LintSmokeTest(TestCase):
        
    def test1(self):
        """make pylint checking itself"""
        Run(['--include-ids=y', 'pylint'], reporter=TextReporter(StringIO()), quiet=1)
    
    def test2(self):
        """make pylint checking itself"""
        Run(['pylint.lint'], reporter=ParseableTextReporter(StringIO()), quiet=1)
    
    def test3(self):
        """make pylint checking itself"""
        Run(['pylint.checkers'], reporter=HTMLReporter(StringIO()), quiet=1)
    
    def test4(self):
        """make pylint checking itself"""
        Run(['pylint.checkers'], reporter=ColorizedTextReporter(StringIO()), quiet=1)
    
    def test5(self):
        """make pylint checking itself"""
        Run(['pylint.checkers'], reporter=VSTextReporter(StringIO()), quiet=1)
    
    def test_generate_config_option(self):
        """make pylint checking itself"""
        sys.stdout = StringIO()
        try:
            self.assertRaises(SystemExit, Run, 
                              ['--generate-rcfile'],
                              reporter=HTMLReporter(StringIO()),
                              quiet=1)
        finally:
            sys.stdout = sys.__stdout__
    
    def test_help_message_option(self):
        """make pylint checking itself"""
        sys.stdout = StringIO()
        try:
            self.assertRaises(SystemExit, Run, 
                              ['--help-msg', 'W0101'],
                              reporter=HTMLReporter(StringIO()),
                              quiet=1)
            self.assertRaises(SystemExit, Run, 
                              ['--help-msg', 'WX101'],
                              reporter=HTMLReporter(StringIO()),
                              quiet=1)
        finally:
            sys.stdout = sys.__stdout__
    
        
if __name__ == '__main__':
    unittest_main()
