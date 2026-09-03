# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import astroid
from astroid import nodes

from pylint.checkers.classes.class_checker import (
    ClassChecker,
    _setattr_names_in_defining_methods,
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


def test_method_hidden_ancestor_attribute_builtin_name(linter: PyLinter) -> None:
    """Regression test for issue 11361: StatementMissing when checking method-hidden

    with a method name matching a builtin on an ancestor without that method.
    """
    checker = ClassChecker(linter)
    checker.open()
    linter.set_current_module("my_mod")
    module = astroid.parse("""
        class C:
            def __init__(self):
                self.help = None

        class D(C):
            def help(self):
                pass
        """)
    method_node = module.body[1].body[0]
    assert isinstance(method_node, nodes.FunctionDef)
    checker.visit_functiondef(method_node)
    assert any(msg.symbol == "method-hidden" for msg in linter.reporter.messages)

    # When ancestor also defines the method, overriding it is allowed
    linter.reporter.messages.clear()
    module2 = astroid.parse("""
        class C:
            def __init__(self):
                self.help = None
            def help(self):
                pass

        class D(C):
            def help(self):
                pass
        """)
    method_node2 = module2.body[1].body[0]
    assert isinstance(method_node2, nodes.FunctionDef)
    checker.visit_functiondef(method_node2)
    assert not any(msg.symbol == "method-hidden" for msg in linter.reporter.messages)
