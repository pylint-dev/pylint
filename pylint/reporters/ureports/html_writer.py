# Copyright (c) 2003-2016 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""HTML formatting drivers for ureports"""

from pylint.reporters.ureports import BaseWriter


class HTMLWriter(BaseWriter):
    """format layouts as HTML"""

    def __init__(self, snippet=None):
        super(HTMLWriter, self).__init__()
        self.snippet = snippet

    def begin_format(self):
        """begin to format a layout"""
        super(HTMLWriter, self).begin_format()
        if self.snippet is None:
            self.writeln(u'<html>')
            self.writeln(u'<body>')

    def end_format(self):
        """finished to format a layout"""
        if self.snippet is None:
            self.writeln(u'</body>')
            self.writeln(u'</html>')

    def visit_section(self, layout):
        """display a section as html, using div + h[section level]"""
        self.section += 1
        self.writeln(u'<div>')
        self.format_children(layout)
        self.writeln(u'</div>')
        self.section -= 1

    def visit_title(self, layout):
        """display a title using <hX>"""
        self.write(u'<h%s>' % self.section)
        self.format_children(layout)
        self.writeln(u'</h%s>' % self.section)

    def visit_table(self, layout):
        """display a table as html"""
        self.writeln(u'<table>')
        table_content = self.get_table_content(layout)
        for i, row in enumerate(table_content):
            if i == 0 and layout.rheaders:
                self.writeln(u'<tr class="header">')
            else:
                self.writeln(u'<tr class="%s">' % (u'even' if i % 2 else u'odd'))
            for j, cell in enumerate(row):
                cell = cell or u'&#160;'
                if (layout.rheaders and i == 0) or \
                   (layout.cheaders and j == 0):
                    self.writeln(u'<th>%s</th>' % cell)
                else:
                    self.writeln(u'<td>%s</td>' % cell)
            self.writeln(u'</tr>')
        self.writeln(u'</table>')

    def visit_paragraph(self, layout):
        """display links (using <p>)"""
        self.write(u'<p>')
        self.format_children(layout)
        self.write(u'</p>')

    def visit_verbatimtext(self, layout):
        """display verbatim text (using <pre>)"""
        self.write(u'<pre>')
        self.write(layout.data.replace(u'&', u'&amp;').replace(u'<', u'&lt;'))
        self.write(u'</pre>')

    def visit_text(self, layout):
        """add some text"""
        data = layout.data
        if layout.escaped:
            data = data.replace(u'&', u'&amp;').replace(u'<', u'&lt;')
        self.write(data)
