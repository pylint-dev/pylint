import sys
import os
from logilab.common.testlib import unittest_main, TestCase
from os.path import exists
from cStringIO import StringIO

from pylint.checkers import initialize, imports
from pylint.lint import PyLinter

from utils import TestReporter

class DependenciesGraphTC(TestCase):
    """test the imports graph function"""

    dest = 'dependencies_graph.dot'
    def tearDown(self):
        os.remove(self.dest)

    def test_dependencies_graph(self):
        imports.dependencies_graph(self.dest, {'labas': ['hoho', 'yep'],
                                               'hoho': ['yep']})
        self.assertEqual(open(self.dest).read().strip(),
                          '''
digraph "dependencies_graph" {
rankdir=LR
charset="utf-8"
URL="." node[shape="box"]
"hoho" [];
"yep" [];
"labas" [];
"yep" -> "hoho" [];
"hoho" -> "labas" [];
"yep" -> "labas" [];
}
'''.strip())

class ImportCheckerTC(TestCase):
    def setUp(self):
        self.linter = l = PyLinter(reporter=TestReporter())
        initialize(l)

    def test_checker_dep_graphs(self):
        l = self.linter
        l.global_set_option('persistent', False)
        l.global_set_option('enable', 'imports')
        l.global_set_option('import-graph', 'import.dot')
        l.global_set_option('ext-import-graph', 'ext_import.dot')
        l.global_set_option('int-import-graph', 'int_import.dot')
        l.global_set_option('int-import-graph', 'int_import.dot')
        # ignore this file causing spurious MemoryError w/ some python version (>=2.3?)
        l.global_set_option('ignore', ('func_unknown_encoding.py',))
        try:
            l.check('input')
            self.assert_(exists('import.dot'))
            self.assert_(exists('ext_import.dot'))
            self.assert_(exists('int_import.dot'))
        finally:
            for fname in ('import.dot', 'ext_import.dot', 'int_import.dot'):
                try:
                    os.remove(fname)
                except:
                    pass

if __name__ == '__main__':
    unittest_main()
