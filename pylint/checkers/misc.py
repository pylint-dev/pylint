# -*- coding: utf-8 -*-
# Copyright (c) 2006, 2009-2013 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012-2014 Google, Inc.
# Copyright (c) 2014-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Alexandru Coman <fcoman@bitdefender.com>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2016 glegoux <gilles.legoux@gmail.com>
# Copyright (c) 2017 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2017 Mikhail Fesenko <proggga@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING


"""Check source code is ascii only or has an encoding declaration (PEP 263)"""

# pylint: disable=W0511

import re

import six

from pylint.interfaces import IRawChecker
from pylint.checkers import BaseChecker
from pylint.utils import OPTION_RGX


MSGS = {
    'W0511': ('%s',
              'fixme',
              'Used when a warning note as FIXME or XXX is detected.'),
    'W0512': ('Cannot decode using encoding "%s",'
              ' unexpected byte at position %d',
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
                {'type': 'csv', 'metavar': '<comma separated values>',
                 'default': ('FIXME', 'XXX', 'TODO'),
                 'help': ('List of note tags to take in consideration, '
                          'separated by a comma.')}),)

    def _check_note(self, notes, lineno, line, module_last_lineno):
        """
        Add the message 'fixme' in case a note is found in the line.

        :param notes: regular expression object matching any notes
                      (XXX, TODO, FIXME) behind a '#'
        :type notes: re.pattern object
        :param lineno: line number
        :type lineno: int
        :param line: line to be checked
        :type line: str
        :param module_last_lineno: last line number of the module as parsed by astroid
                                   (may be different from real last line number in case
                                    commented lines exist at the end of the module)
        :type module_last_lineno: int
        """
        # First, simply check if the notes are in the line at all. This is an
        # optimisation to prevent using the regular expression on every line,
        # but rather only on lines which may actually contain one of the notes.
        # This prevents a pathological problem with lines that are hundreds
        # of thousands of characters long.
        for note in self.config.notes:
            if note in line:
                break
        else:
            return

        match = notes.search(line)
        if not match:
            return
        # In case the module ends with commented lines, the astroid parser
        # don't take into account those lines, then:
        # - the line number of those lines is greater than the
        #   module last line number (module.tolineno)
        # - astroid module object can't inform pylint
        #   of disabled messages in those extra lines.
        if lineno > module_last_lineno:
            disable_option_match = OPTION_RGX.search(line)
            if disable_option_match:
                try:
                    _, value = disable_option_match.group(1).split('=', 1)
                    values = [_val.strip().upper() for _val in value.split(',')]
                    if set(values) & set(self.config.notes):
                        return
                except ValueError:
                    self.add_message('bad-inline-option',
                                     args=disable_option_match.group(1).strip(), line=line)
                    return
        self.add_message('fixme', args=line[match.start(1):].rstrip(), line=lineno)

    def _check_encoding(self, lineno, line, file_encoding):
        try:
            return six.text_type(line, file_encoding)
        except UnicodeDecodeError as ex:
            self.add_message('invalid-encoded-data', line=lineno,
                             args=(file_encoding, ex.args[2]))
        except LookupError as ex:
            if (line.startswith('#') and
                    "coding" in line and file_encoding in line):
                self.add_message('syntax-error',
                                 line=lineno,
                                 args='Cannot decode using encoding "{}",'
                                      ' bad encoding'.format(file_encoding))

    def process_module(self, module):
        """inspect the source file to find encoding problem or fixmes like
        notes
        """
        if self.config.notes:
            notes = re.compile(
                r'.*?#\s*(%s)(:*\s*.*)' % "|".join(self.config.notes))
        else:
            notes = None
        if module.file_encoding:
            encoding = module.file_encoding
        else:
            encoding = 'ascii'

        with module.stream() as stream:
            for lineno, line in enumerate(stream):
                line = self._check_encoding(lineno + 1, line, encoding)
                if line is not None and notes:
                    self._check_note(notes, lineno + 1, line, module.tolineno)


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(EncodingChecker(linter))
