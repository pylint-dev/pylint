import sys
import os
import unittest
from os.path import exists
from cStringIO import StringIO

from pylint.checkers import initialize, imports
from pylint.lint import PyLinter

from utils import TestReporter

class DependenciesGraphTC(unittest.TestCase):
    """test the imports graph function"""

    dest = 'dependencies_graph.dot'
    def tearDown(self):
        os.remove(self.dest)
        
    def test_dependencies_graph(self):
        imports.dependencies_graph(self.dest, {'labas': ['hoho', 'yep'],
                                               'hoho': ['yep']})
        self.assertEquals(open(self.dest).read().strip(),
                          '''
digraph g {
rankdir="LR" URL="." concentrate=false
edge[fontsize="10" ]
node[width="0" height="0" fontsize="12" fontcolor="black"]
"hoho" [ label="hoho" ];
"yep" [ label="yep" ];
"labas" [ label="labas" ];
"yep" -> "hoho" [ ] ;
"hoho" -> "labas" [ ] ;
"yep" -> "labas" [ ] ;
}
'''.strip())
                          
class ImportCheckerTC(unittest.TestCase):
    def setUp(self):
        self.linter = l = PyLinter(reporter=TestReporter())
        initialize(l)
        for checker in l._checkers:
            checker.enable(False)
        
    def test_checker_dep_graphs(self):
        l = self.linter
        l.global_set_option('persistent', False)
        l.global_set_option('enable-checker', 'imports')
        l.global_set_option('import-graph', 'import.dot')
        l.global_set_option('ext-import-graph', 'ext_import.dot')
        l.global_set_option('int-import-graph', 'int_import.dot')
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
    unittest.main()
