# Copyright (c) 2007 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""RPython linter class"""

from logilab.common.interface import implements
from logilab.common.fileutils import norm_open

from pylint.lint import PyLinter
from pylint.interfaces import IASTNGChecker

class RPyLinter(PyLinter):
    """the RPyLinter handle analysis differently than the standar PyLinter to
    be more close to the pypy translation process
    """

    def __init__(self, *args, **kwargs):
        PyLinter.__init__(self, *args, **kwargs)
        # enable the rpython checker which is disabled by default
        from pylint.checkers.rpython import RPythonChecker
        RPythonChecker.enabled = True
        # XXX disable reports
        # XXX set parseable format

    def check(self, files_or_modules):
        """main checking entry: check a list of files or modules from their
        name.
        """
        raise Exception()
        if len(files_or_modules) > 1:
            raise Exception('only one module can be analyzed in rpython mode')
        PyLinter.check(self, files_or_modules)
        

    def check_astng_module(self, astng, checkers):
        """check a module from its astng representation, real work"""
        # call raw checkers if possible
        if not astng.pure_python:
            raise Exception('only python modules can be analyzed in rpython mode')
        # search target
        targets = astng.locals()['target']
        if len(targets) > 1:
            raise Exception('more than one target found')
        target = targets[0]
        if not target.callable():
            raise Exception('non callable target')
        # check target return 2 to 3 values : entry point, None (hum?) [, annotator policy]
        returns = list(target.infer_call_result())
        if len(returns) > 1:
            raise Exception('target has more than one return')
        print returns
        return
        
        # search entry point
        entry = astng
        stream = norm_open(astng.file)
        # invoke IRawChecker interface on self to fetch module/block
        # level options
        self.process_module(stream)
        if self._ignore_file:
            return False
        # walk ast to collect line numbers
        orig_state = self._module_msgs_state.copy()
        self._module_msgs_state = {}
        self.collect_block_lines(astng, orig_state)
        # XXX forget raw check for now
        #for checker in checkers:
        #    if implements(checker, IRawChecker) and checker is not self:
        #        stream.seek(0)
        #        checker.process_module(stream)
        # generate events to astng checkers
        self.astng_events(astng, [checker for checker in checkers
                                  if implements(checker, IASTNGChecker)])
        
        # always return to avoid package recursion
        return False
                            
