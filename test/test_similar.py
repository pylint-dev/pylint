import sys
from logilab.common.testlib import TestCase, unittest_main

from cStringIO import StringIO
from os.path import join, dirname, abspath

from pylint.checkers import similar

SIMILAR1 = join(dirname(abspath(__file__)), 'input', 'similar1')
SIMILAR2 = join(dirname(abspath(__file__)), 'input', 'similar2')

class SimilarTC(TestCase):
    """test the similar command line utility"""

    def test_ignore_comments(self):
        sys.stdout = StringIO()
        try:
            similar.run(['--ignore-comments', SIMILAR1, SIMILAR2])
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        self.assertMultiLineEqual(output.strip(), ("""
7 similar lines in 2 files
==%s:5
==%s:5
   same file as this one. 
   more than 4
   identical lines should
   be
   detected
   
   
TOTAL lines=38 duplicates=7 percent=18.42
""" % (SIMILAR1, SIMILAR2)).strip())


    def test_dont_ignore_comments(self):
        sys.stdout = StringIO()
        try:
            similar.run([SIMILAR1, SIMILAR2])
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = sys.__stdout__
        self.assertMultiLineEqual(output.strip(), """
TOTAL lines=38 duplicates=0 percent=0.00
        """.strip())

    def test_help(self):
        sys.stdout = StringIO()
        try:
            try:
                similar.run(['--help'])
            except SystemExit, ex:
                self.assertEqual(ex.code, 0)
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
                self.assertEqual(ex.code, 1)
            else:
                self.fail()
        finally:
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest_main()
