# Copyright (c) 2006-2008, 2010, 2013 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012 FELD Boris <lothiraldan@gmail.com>
# Copyright (c) 2014-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Reverb C <reverbc@users.noreply.github.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Damien Baty <damien.baty@polyconseil.fr>
# Copyright (c) 2020 Frank Harrison <frank@doublethefish.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Andrew Howe <howeaj@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# pylint: disable=redefined-outer-name

import os
import shutil
from os.path import exists

import pytest

from pylint import testutils
from pylint.checkers import imports, initialize
from pylint.lint import PyLinter


@pytest.fixture
def dest(request):
    dest = request.param
    yield dest
    try:
        os.remove(dest)
    except FileNotFoundError:
        # file may not have been created if tests inside fixture skipped
        pass


POSSIBLE_DOT_FILENAMES = ["foo.dot", "foo.gv", "tests/regrtest_data/foo.dot"]


@pytest.mark.parametrize("dest", POSSIBLE_DOT_FILENAMES, indirect=True)
def test_dependencies_graph(dest):
    """DOC files are correctly generated, and the graphname is the basename"""
    imports._dependencies_graph(dest, {"labas": ["hoho", "yep"], "hoho": ["yep"]})
    with open(dest, encoding="utf-8") as stream:
        assert (
            stream.read().strip()
            == """
digraph "foo" {
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
""".strip()
        )


@pytest.mark.parametrize("filename", ["graph.png", "graph"])
@pytest.mark.skipif(
    any(shutil.which(x) for x in ("dot", "gv")), reason="dot or gv is installed"
)
def test_missing_graphviz(filename):
    """Raises if graphviz is not installed, and defaults to png if no extension given"""
    with pytest.raises(RuntimeError, match=r"Cannot generate `graph\.png`.*"):
        imports._dependencies_graph(filename, {"a": ["b", "c"], "b": ["c"]})


@pytest.fixture
def linter():
    pylinter = PyLinter(reporter=testutils.GenericTestReporter())
    initialize(pylinter)
    return pylinter


@pytest.fixture
def remove_files():
    yield
    for fname in ("import.dot", "ext_import.dot", "int_import.dot"):
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass


@pytest.mark.usefixtures("remove_files")
def test_checker_dep_graphs(linter):
    linter.global_set_option("persistent", False)
    linter.global_set_option("reports", True)
    linter.global_set_option("enable", "imports")
    linter.global_set_option("import-graph", "import.dot")
    linter.global_set_option("ext-import-graph", "ext_import.dot")
    linter.global_set_option("int-import-graph", "int_import.dot")
    linter.global_set_option("int-import-graph", "int_import.dot")
    # ignore this file causing spurious MemoryError w/ some python version (>=2.3?)
    linter.global_set_option("ignore", ("func_unknown_encoding.py",))
    linter.check("input")
    linter.generate_reports()
    assert exists("import.dot")
    assert exists("ext_import.dot")
    assert exists("int_import.dot")
