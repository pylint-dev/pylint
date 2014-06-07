# pylint: disable=W0511
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
""" Copyright (c) 2000-2010 LOGILAB S.A. (Paris, FRANCE).
 http://www.logilab.fr/ -- mailto:contact@logilab.fr

Check source code is ascii only or has an encoding declaration (PEP 263)
"""

import re

from pylint.interfaces import IRawChecker
from pylint.checkers import BaseChecker


MSGS = {
    'W0511': ('%s',
              'fixme',
              'Used when a warning note as FIXME or XXX is detected.'),
    'W0512': ('Cannot decode using encoding "%s", unexpected byte at position %d',
              'invalid-encoded-data',
              'Used when a source line cannot be decoded using the specified '
              'source file encoding.',
              {'maxversion': (3, 0)}),
    }


class EncodingChecker(BaseChecker):
    """checks for:
    * warning notes in the code like FIXME, XXX
    * encoding issues.
    """
    __implements__ = IRawChecker

    # configuration section name
    name = 'miscellaneous'
    msgs = MSGS

    options = (('notes',
                {'type' : 'csv', 'metavar' : '<comma separated values>',
                 'default' : ('FIXME', 'XXX', 'TODO'),
                 'help' : 'List of note tags to take in consideration, \
separated by a comma.'
                 }),
               )

    def _check_note(self, notes, lineno, line):
        match = notes.search(line)
        if match:
            self.add_message('fixme', args=line[match.start():-1], line=lineno)

    def _check_encoding(self, lineno, line, file_encoding):
        try:
            return unicode(line, file_encoding)
        except UnicodeDecodeError, ex:
            self.add_message('invalid-encoded-data', line=lineno,
                             args=(file_encoding, ex.args[2]))

    def process_module(self, module):
        """inspect the source file to find encoding problem or fixmes like
        notes
        """
        stream = module.file_stream
        stream.seek(0) # XXX may be removed with astroid > 0.23
        if self.config.notes:
            notes = re.compile('|'.join(self.config.notes))
        else:
            notes = None
        if module.file_encoding:
            encoding = module.file_encoding
        else:
            encoding = 'ascii'
        for lineno, line in enumerate(stream):
            line = self._check_encoding(lineno+1, line, encoding)
            if line is not None and notes:
                self._check_note(notes, lineno+1, line)

def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(EncodingChecker(linter))
