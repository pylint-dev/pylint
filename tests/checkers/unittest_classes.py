# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import astroid
from astroid import nodes

from pylint.checkers.classes.class_checker import (
    ClassChecker,
    _setattr_in_defining_methods,
)
from pylint.lint import PyLinter


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


def test_setattr_in_defining_methods_ignores_metaclass() -> None:
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
    assert not _setattr_in_defining_methods(meta, "banana", ("__init__",))
    assert _setattr_in_defining_methods(plain, "banana", ("__init__",))
