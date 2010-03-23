# pylint: disable-msg=W0511
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
""" Copyright (c) 2000-2010 LOGILAB S.A. (Paris, FRANCE).
 http://www.logilab.fr/ -- mailto:contact@logilab.fr

Check source code is ascii only or has an encoding declaration (PEP 263)
"""

import re

from pylint.interfaces import IRawChecker
from pylint.checkers import BaseChecker

def is_ascii(string):
    """return true if non ascii characters are detected in the given string
    and line number where non-ascii has been encountered.
    """
    for i, line in enumerate(string.splitlines()):
        if line and max([ord(char) for char in line]) >= 128:
            return False, i + 1
    return True, 0
    
# regexp matching both emacs and vim declaration
ENCODING_RGX = re.compile("[^#]*#*.*coding[:=]\s*([^\s]+)")

def guess_encoding(string):
    """try to guess encoding from a python file as string
    return None if not found
    """
    assert type(string) is type(''), type(string)
    # check for UTF-8 byte-order mark
    if string.startswith('\xef\xbb\xbf'):
        return 'UTF-8'
    first_lines = string.split('\n', 2)[:2]
    for line in first_lines:
        # check for emacs / vim encoding declaration
        match = ENCODING_RGX.match(line)
        if match is not None:
            return match.group(1)

        
MSGS = {
    'E0501': ('Non ascii characters found but no encoding specified (PEP 263)',
              'Used when some non ascii characters are detected but now \
              encoding is specified, as explicited in the PEP 263.'),
    'E0502': ('Wrong encoding specified (%s)',
              'Used when a known encoding is specified but the file doesn\'t \
              seem to be actually in this encoding.'),
    'E0503': ('Unknown encoding specified (%s)',
              'Used when an encoding is specified, but it\'s unknown to Python.'
              ),
    
    'W0511': ('%s',
              'Used when a warning note as FIXME or XXX is detected.'),
    }

class EncodingChecker(BaseChecker):
    """checks for:                                                             
    * warning notes in the code like FIXME, XXX                                
    * PEP 263: source code with non ascii character but no encoding declaration
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

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
    
    def process_module(self, stream):
        """inspect the source file to found encoding problem or fixmes like
        notes
        """
        # source encoding
        data = stream.read()
        ascii, lineno = is_ascii(data)
        if not ascii:
            encoding = guess_encoding(data)
            if encoding is None:
                self.add_message('E0501', line=lineno)
            else:
                try:
                    unicode(data, encoding)
                except UnicodeError:
                    self.add_message('E0502', args=encoding, line=1)
                except LookupError:
                    self.add_message('E0503', args=encoding, line=1)
        del data
        # warning notes in the code
        stream.seek(0)
        notes = []
        for note in self.config.notes:
            notes.append(re.compile(note))
        linenum = 1
        for line in stream.readlines():
            for note in notes:
                match = note.search(line)
                if match:
                    self.add_message('W0511', args=line[match.start():-1],
                                     line=linenum)
                    break
            linenum += 1
                    
                
            
def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(EncodingChecker(linter))
