# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import sys
from pathlib import Path

import astroid
import pytest
from astroid import nodes

from pylint.checkers.classes.class_checker import (
    ClassChecker,
    _setattr_names_in_defining_methods,
)
from pylint.lint import PyLinter, Run
from pylint.reporters import CollectingReporter


def test_attribute_defined_outside_init_disabled(linter: PyLinter) -> None:
    checker = ClassChecker(linter)
    checker.open()
    klass = astroid.extract_node("class Example: pass")
    assert isinstance(klass, nodes.ClassDef)
    checker._setattr_attrs[klass] = {}
    linter.disable("attribute-defined-outside-init")

    checker._check_attribute_defined_outside_init(klass)

    assert klass not in checker._setattr_attrs


def test_visit_call_ignores_setattr_outside_method(linter: PyLinter) -> None:
    checker = ClassChecker(linter)
    call = astroid.extract_node('setattr(object(), "banana", 1)')
    assert isinstance(call, nodes.Call)

    checker.visit_call(call)

    assert not checker._setattr_attrs


def test_setattr_names_in_defining_methods_ignores_metaclass() -> None:
    module = astroid.parse("""
        class Meta(type):
            def __init__(cls):
                setattr(cls, "banana", 1)

        class Plain:
            def __init__(self):
                setattr(self, "banana", 1)
        """)
    meta, plain = module.body[0], module.body[1]

    assert isinstance(meta, nodes.ClassDef) and isinstance(plain, nodes.ClassDef)
    assert _setattr_names_in_defining_methods(meta, ("__init__",)) == set()
    assert _setattr_names_in_defining_methods(plain, ("__init__",)) == {"banana"}


SUPER_INIT_STUB_CODE = """class Foo:
    def __init__(self) -> None: ...

class Bar(Foo):
    def __init__(self) -> None: ...
"""


@pytest.mark.parametrize(
    ("suffix", "expected"),
    [(".pyi", []), (".py", ["super-init-not-called"])],
    ids=["stub", "module"],
)
def test_super_init_not_called_is_not_raised_in_a_stub(
    tmp_path: Path, suffix: str, expected: list[str]
) -> None:
    """A ``.pyi`` ``__init__`` is ``...``, so it cannot call the parent's (#9096)."""
    path = tmp_path / f"foo{suffix}"
    path.write_text(SUPER_INIT_STUB_CODE, encoding="utf-8")
    run = Run(
        ["--disable=all", "--enable=super-init-not-called", str(path)],
        reporter=CollectingReporter(),
        exit=False,
    )
    assert [message.symbol for message in run.linter.reporter.messages] == expected


@pytest.mark.parametrize(
    "code",
    [
        "class C(slice(1, 2)):\n    pass\n",
        pytest.param(
            "from typing import Unpack\nclass C(Unpack()[:]):\n    pass\n",
            marks=pytest.mark.skipif(
                sys.version_info < (3, 11),
                reason="typing.Unpack was introduced in Python 3.11",
            ),
        ),
    ],
    ids=["slice_call", "unpack_slice"],
)
def test_slice_base_does_not_crash(tmp_path: Path, code: str) -> None:
    """Regression test for issue 11609: slice base expression should not crash."""
    path = tmp_path / "foo.py"
    path.write_text(code, encoding="utf-8")
    run = Run(
        ["--disable=all", "--enable=inherit-non-class", str(path)],
        reporter=CollectingReporter(),
        exit=False,
    )
    assert [message.symbol for message in run.linter.reporter.messages] == [
        "inherit-non-class"
    ]
