# Copyright (c) 2000-2008 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
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
"""
unittest for visitors.diadefs and extensions.diadefslib modules
"""

from os.path import abspath, dirname, join
from logilab.astng.inspector import Linker
from logilab.common.testlib import TestCase, unittest_main

from pylint.pyreverse.diadefslib import DefaultDiadefGenerator, DiadefsHandler
from pylint.pyreverse.diagrams import set_counter
from pylint.pyreverse.writer import DotWriter

from pylint.pyreverse.utils import get_visibility
from utils import FileTC, build_file_case, get_project, Config

project = get_project(join(dirname(abspath(__file__)), 'data'))
linker = Linker(project)
set_counter(0)

config = Config()

handler = DiadefsHandler(config)
dd = DefaultDiadefGenerator(linker, handler).visit(project)
for diagram in dd:
    diagram.extract_relationships()

class DotWriterTC(FileTC):

    generated_files = ('packages_No_Name.dot', 'classes_No_Name.dot',)
    def setUp(self):
        FileTC.setUp(self)
        writer = DotWriter(config)
        writer.write(dd)
        
build_file_case(DotWriterTC)


class GetVisibilityTC(TestCase):

    def test_special(self):
        for name in ["__reduce_ex__",  "__setattr__"]:
            self.assertEqual(get_visibility(name), 'special')

    def test_private(self):
        for name in ["__g_", "____dsf", "__23_9"]:
            got = get_visibility(name)
            self.assertEqual(got, 'private',
                              'got %s instead of private for value %s' % (got, name))

    def test_public(self):
        self.assertEqual(get_visibility('simple'), 'public')

    def test_protected(self):
        for name in ["_","__", "___", "____", "_____", "___e__", "_nextsimple", "_filter_it_"]:
            got = get_visibility(name)
            self.assertEqual(got, 'protected',
                              'got %s instead of protected for value %s' % (got, name))


if __name__ == '__main__':
    unittest_main()
