# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING


import re

from pylint.lint.expand_modules import _basename_in_ignore_list_re


def test__basename_in_ignore_list_re_match():
    patterns = [re.compile(".*enchilada.*"), re.compile("unittest_.*")]
    assert _basename_in_ignore_list_re("unittest_utils.py", patterns)
    assert _basename_in_ignore_list_re("cheese_enchiladas.xml", patterns)


def test__basename_in_ignore_list_re_nomatch():
    patterns = [re.compile(".*enchilada.*"), re.compile("unittest_.*")]
    assert not _basename_in_ignore_list_re("test_utils.py", patterns)
    assert not _basename_in_ignore_list_re("enchilad.py", patterns)
