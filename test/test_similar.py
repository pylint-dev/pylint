import sys
import unittest
from cStringIO import StringIO

from pylint.checkers import similar


class SimilarTC(unittest.TestCase):
    """test the similar command line utility"""
    def test(self):
        sys.stdout = StringIO()
        try:
            similar.run(['--ignore-comments', 'input/similar1', 'input/similar2'])
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        self.assertEquals(output.strip(), """
7 similar lines in 2 files
==input/similar1:5
==input/similar2:5
   same file as this one. 
   more than 4
   identical lines should
   be
   detected
   
   
TOTAL lines=38 duplicates=7 percent=0.184210526316        
""".strip())
                          
    def test_help(self):
        sys.stdout = StringIO()
        try:
            try:
                similar.run(['--help'])
            except SystemExit, ex:
                self.assertEquals(ex.code, 0)
            else:
                self.fail()
        finally:
            sys.stdout = sys.__stdout__

    def test_no_args(self):
        sys.stdout = StringIO()
        try:
            try:
                similar.run([])
            except SystemExit, ex:
                self.assertEquals(ex.code, 1)
            else:
                self.fail()
        finally:
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
