import sys
from os.path import join, dirname, abspath
import unittest

import six

from pylint.checkers import similar

SIMILAR1 = join(dirname(abspath(__file__)), 'input', 'similar1')
SIMILAR2 = join(dirname(abspath(__file__)), 'input', 'similar2')

class SimilarTC(unittest.TestCase):
    """test the similar command line utility"""

    def test_ignore_comments(self):
        sys.stdout = six.StringIO()
        try:
            similar.Run(['--ignore-comments', SIMILAR1, SIMILAR2])
        except SystemExit as ex:
            self.assertEqual(ex.code, 0)
            output = sys.stdout.getvalue()
        else:
            self.fail('not system exit')
        finally:
            sys.stdout = sys.__stdout__
        self.assertMultiLineEqual(output.strip(), ("""
10 similar lines in 2 files
==%s:0
==%s:0
   import one
   from two import two
   three
   four
   five
   six
   seven
   eight
   nine
   ''' ten
TOTAL lines=44 duplicates=10 percent=22.73
""" % (SIMILAR1, SIMILAR2)).strip())


    def test_ignore_docsrings(self):
        sys.stdout = six.StringIO()
        try:
            similar.Run(['--ignore-docstrings', SIMILAR1, SIMILAR2])
        except SystemExit as ex:
            self.assertEqual(ex.code, 0)
            output = sys.stdout.getvalue()
        else:
            self.fail('not system exit')
        finally:
            sys.stdout = sys.__stdout__
        self.assertMultiLineEqual(output.strip(), ("""
8 similar lines in 2 files
==%s:6
==%s:6
   seven
   eight
   nine
   ''' ten
   ELEVEN
   twelve '''
   thirteen
   fourteen

5 similar lines in 2 files
==%s:0
==%s:0
   import one
   from two import two
   three
   four
   five
TOTAL lines=44 duplicates=13 percent=29.55
""" % ((SIMILAR1, SIMILAR2) * 2)).strip())


    def test_ignore_imports(self):
        sys.stdout = six.StringIO()
        try:
            similar.Run(['--ignore-imports', SIMILAR1, SIMILAR2])
        except SystemExit as ex:
            self.assertEqual(ex.code, 0)
            output = sys.stdout.getvalue()
        else:
            self.fail('not system exit')
        finally:
            sys.stdout = sys.__stdout__
        self.assertMultiLineEqual(output.strip(), """
TOTAL lines=44 duplicates=0 percent=0.00
""".strip())


    def test_ignore_nothing(self):
        sys.stdout = six.StringIO()
        try:
            similar.Run([SIMILAR1, SIMILAR2])
        except SystemExit as ex:
            self.assertEqual(ex.code, 0)
            output = sys.stdout.getvalue()
        else:
            self.fail('not system exit')
        finally:
            sys.stdout = sys.__stdout__
        self.assertMultiLineEqual(output.strip(), ("""
5 similar lines in 2 files
==%s:0
==%s:0
   import one
   from two import two
   three
   four
   five
TOTAL lines=44 duplicates=5 percent=11.36
""" % (SIMILAR1, SIMILAR2)).strip())

    def test_help(self):
        sys.stdout = six.StringIO()
        try:
            similar.Run(['--help'])
        except SystemExit as ex:
            self.assertEqual(ex.code, 0)
        else:
            self.fail('not system exit')
        finally:
            sys.stdout = sys.__stdout__

    def test_no_args(self):
        sys.stdout = six.StringIO()
        try:
            similar.Run([])
        except SystemExit as ex:
            self.assertEqual(ex.code, 1)
        else:
            self.fail('not system exit')
        finally:
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
