# Copyright (c) 2010, 2012, 2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012 Ry4an Brase <ry4an-hg@ry4an.org>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import sys
from os.path import join, dirname, abspath
from contextlib import redirect_stdout

from io import StringIO
import pytest

from pylint.checkers import similar

SIMILAR1 = join(dirname(abspath(__file__)), 'input', 'similar1')
SIMILAR2 = join(dirname(abspath(__file__)), 'input', 'similar2')


def test_ignore_comments():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(['--ignore-comments', SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == ("""
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
""" % (SIMILAR1, SIMILAR2)).strip()


def test_ignore_docsrings():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(['--ignore-docstrings', SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == ("""
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
""" % ((SIMILAR1, SIMILAR2) * 2)).strip()


def test_ignore_imports():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run(['--ignore-imports', SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == """
TOTAL lines=44 duplicates=0 percent=0.00
""".strip()


def test_ignore_nothing():
    output = StringIO()
    with redirect_stdout(output), pytest.raises(SystemExit) as ex:
        similar.Run([SIMILAR1, SIMILAR2])
    assert ex.value.code == 0
    assert output.getvalue().strip() == ("""
5 similar lines in 2 files
==%s:0
==%s:0
   import one
   from two import two
   three
   four
   five
TOTAL lines=44 duplicates=5 percent=11.36
""" % (SIMILAR1, SIMILAR2)).strip()


def test_help():
    output = StringIO()
    with redirect_stdout(output):
        try:
            similar.Run(['--help'])
        except SystemExit as ex:
            assert ex.code == 0
        else:
            pytest.fail('not system exit')


def test_no_args():
    output = StringIO()
    with redirect_stdout(output):
        try:
            similar.Run([])
        except SystemExit as ex:
            assert ex.code == 1
        else:
            pytest.fail('not system exit')
