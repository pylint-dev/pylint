# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2016 Glenn Matthews <glenn@e-dad.net>
# Copyright (c) 2017-2019, 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2017-2018, 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2017 ttenhoeve-aa <ttenhoeve@appannie.com>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import io
import re

from pylint.utils import utils


def test__basename_in_blacklist_re_match():
    patterns = [re.compile(".*enchilada.*"), re.compile("unittest_.*")]
    assert utils._basename_in_blacklist_re("unittest_utils.py", patterns)
    assert utils._basename_in_blacklist_re("cheese_enchiladas.xml", patterns)


def test__basename_in_blacklist_re_nomatch():
    patterns = [re.compile(".*enchilada.*"), re.compile("unittest_.*")]
    assert not utils._basename_in_blacklist_re("test_utils.py", patterns)
    assert not utils._basename_in_blacklist_re("enchilad.py", patterns)


def test_decoding_stream_unknown_encoding():
    """decoding_stream should fall back to *some* decoding when given an
    unknown encoding.
    """
    binary_io = io.BytesIO(b"foo\nbar")
    stream = utils.decoding_stream(binary_io, "garbage-encoding")
    # should still act like a StreamReader
    ret = stream.readlines()
    assert ret == ["foo\n", "bar"]


def test_decoding_stream_known_encoding():
    binary_io = io.BytesIO("€".encode("cp1252"))
    stream = utils.decoding_stream(binary_io, "cp1252")
    assert stream.read() == "€"
