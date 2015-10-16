# copyright 2003-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-common.
#
# pylint is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# pylint is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with pylint.  If not, see <http://www.gnu.org/licenses/>.
"""Text formatting drivers for ureports"""

from __future__ import print_function

from pylint.reporters.ureports import BaseWriter


TITLE_UNDERLINES = [u'', u'=', u'-', u'`', u'.', u'~', u'^']
BULLETS = [u'*', u'-']

class TextWriter(BaseWriter):
    """format layouts as text
    (ReStructured inspiration but not totally handled yet)
    """
    def begin_format(self):
        super(TextWriter, self).begin_format()
        self.list_level = 0

    def visit_section(self, layout):
        """display a section as text
        """
        self.section += 1
        self.writeln()
        self.format_children(layout)
        self.section -= 1
        self.writeln()

    def visit_title(self, layout):
        title = u''.join(list(self.compute_content(layout)))
        self.writeln(title)
        try:
            self.writeln(TITLE_UNDERLINES[self.section] * len(title))
        except IndexError:
            print("FIXME TITLE TOO DEEP. TURNING TITLE INTO TEXT")

    def visit_paragraph(self, layout):
        """enter a paragraph"""
        self.format_children(layout)
        self.writeln()

    def visit_table(self, layout):
        """display a table as text"""
        table_content = self.get_table_content(layout)
        # get columns width
        cols_width = [0]*len(table_content[0])
        for row in table_content:
            for index, col in enumerate(row):
                cols_width[index] = max(cols_width[index], len(col))
        self.default_table(layout, table_content, cols_width)
        self.writeln()

    def default_table(self, layout, table_content, cols_width):
        """format a table"""
        cols_width = [size+1 for size in cols_width]
        format_strings = u' '.join([u'%%-%ss'] * len(cols_width))
        format_strings = format_strings % tuple(cols_width)
        format_strings = format_strings.split(u' ')
        table_linesep = u'\n+' + u'+'.join([u'-'*w for w in cols_width]) + u'+\n'
        headsep = u'\n+' + u'+'.join([u'='*w for w in cols_width]) + u'+\n'
        # FIXME: layout.cheaders
        self.write(table_linesep)
        for index, line in enumerate(table_content):
            self.write(u'|')
            for line_index, at_index in enumerate(line):
                self.write(format_strings[line_index] % at_index)
                self.write(u'|')
            if index == 0 and layout.rheaders:
                self.write(headsep)
            else:
                self.write(table_linesep)

    def visit_verbatimtext(self, layout):
        """display a verbatim layout as text (so difficult ;)
        """
        self.writeln(u'::\n')
        for line in layout.data.splitlines():
            self.writeln(u'    ' + line)
        self.writeln()

    def visit_text(self, layout):
        """add some text"""
        self.write(u'%s' % layout.data)
