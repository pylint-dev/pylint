# copyright 2003-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of pylint.
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
"""Universal report objects and some formatting drivers.

A way to create simple reports using python objects, primarily designed to be
formatted as text and html.
"""
import os
import sys

import six


class BaseWriter(object):
    """base class for ureport writers"""

    def format(self, layout, stream=None, encoding=None):
        """format and write the given layout into the stream object

        unicode policy: unicode strings may be found in the layout;
        try to call stream.write with it, but give it back encoded using
        the given encoding if it fails
        """
        if stream is None:
            stream = sys.stdout
        if not encoding:
            encoding = getattr(stream, 'encoding', 'UTF-8')
        self.encoding = encoding or 'UTF-8'
        self.out = stream
        self.begin_format()
        layout.accept(self)
        self.end_format()

    def format_children(self, layout):
        """recurse on the layout children and call their accept method
        (see the Visitor pattern)
        """
        for child in getattr(layout, 'children', ()):
            child.accept(self)

    def writeln(self, string=u''):
        """write a line in the output buffer"""
        self.write(string + os.linesep)

    def write(self, string):
        """write a string in the output buffer"""
        self.out.write(string)

    def begin_format(self):
        """begin to format a layout"""
        self.section = 0

    def end_format(self):
        """finished to format a layout"""

    def get_table_content(self, table):
        """trick to get table content without actually writing it

        return an aligned list of lists containing table cells values as string
        """
        result = [[]]
        cols = table.cols
        for cell in self.compute_content(table):
            if cols == 0:
                result.append([])
                cols = table.cols
            cols -= 1
            result[-1].append(cell)
        # fill missing cells
        while len(result[-1]) < cols:
            result[-1].append(u'')
        return result

    def compute_content(self, layout):
        """trick to compute the formatting of children layout before actually
        writing it

        return an iterator on strings (one for each child element)
        """
        # Patch the underlying output stream with a fresh-generated stream,
        # which is used to store a temporary representation of a child
        # node.
        out = self.out
        try:
            for child in layout.children:
                stream = six.StringIO()
                self.out = stream
                child.accept(self)
                yield stream.getvalue()
        finally:
            self.out = out
