# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=redefined-outer-name

from __future__ import annotations

import os
import shutil
from collections.abc import Iterator
from os.path import exists

import pytest
from _pytest.fixtures import SubRequest

from pylint import testutils
from pylint.checkers import imports, initialize
from pylint.lint import PyLinter


@pytest.fixture
def dest(request: SubRequest) -> Iterator[str]:
    dest = request.param
    yield dest
    try:
        os.remove(dest)
    except FileNotFoundError:
        # file may not have been created if tests inside fixture skipped
        pass


POSSIBLE_DOT_FILENAMES = ["foo.dot", "foo.gv", "tests/regrtest_data/foo.dot"]


@pytest.mark.parametrize("dest", POSSIBLE_DOT_FILENAMES, indirect=True)
def test_dependencies_graph(dest: str) -> None:
    """DOC files are correctly generated, and the graphname is the basename."""
    imports._dependencies_graph(dest, {"labas": {"hoho", "yep"}, "hoho": {"yep"}})
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
def test_missing_graphviz(filename: str) -> None:
    """Raises if graphviz is not installed, and defaults to png if no extension given."""
    with pytest.raises(RuntimeError, match=r"Cannot generate `graph\.png`.*"):
        imports._dependencies_graph(filename, {"a": {"b", "c"}, "b": {"c"}})


@pytest.fixture
def linter() -> PyLinter:
    pylinter = PyLinter(reporter=testutils.GenericTestReporter())
    initialize(pylinter)
    return pylinter


@pytest.fixture
def remove_files() -> Iterator[None]:
    yield
    for fname in ("import.dot", "ext_import.dot", "int_import.dot"):
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass


@pytest.mark.usefixtures("remove_files")
def test_checker_dep_graphs(linter: PyLinter) -> None:
    linter.set_option("persistent", False)
    linter.set_option("reports", True)
    linter.set_option("enable", "imports")
    linter.set_option("import_graph", "import.dot")
    linter.set_option("ext_import_graph", "ext_import.dot")
    linter.set_option("int_import_graph", "int_import.dot")
    linter.check(["input"])
    linter.generate_reports()
    assert exists("import.dot")
    assert exists("ext_import.dot")
    assert exists("int_import.dot")
