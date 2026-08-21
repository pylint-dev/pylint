# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the pylint.checkers.utils module."""

from __future__ import annotations

import astroid
import pytest
from astroid import nodes

from pylint.checkers import utils


@pytest.mark.parametrize(
    "name,expected",
    [
        ("min", True),
        ("__builtins__", True),
        ("__path__", False),
        ("__file__", False),
        ("whatever", False),
        ("mybuiltin", False),
    ],
)
def testIsBuiltin(name: str, expected: bool) -> None:
    assert utils.is_builtin(name) == expected


@pytest.mark.parametrize(
    "fn,kw",
    [("foo(3)", {"keyword": "bar"}), ("foo(one=a, two=b, three=c)", {"position": 1})],
)
def testGetArgumentFromCallError(fn: str, kw: dict[str, int] | dict[str, str]) -> None:
    with pytest.raises(utils.NoSuchArgumentError):
        node = astroid.extract_node(fn)
        utils.get_argument_from_call(node, **kw)


@pytest.mark.parametrize(
    "fn,kw", [("foo(bar=3)", {"keyword": "bar"}), ("foo(a, b, c)", {"position": 1})]
)
def testGetArgumentFromCallExists(fn: str, kw: dict[str, int] | dict[str, str]) -> None:
    node = astroid.extract_node(fn)
    assert utils.get_argument_from_call(node, **kw) is not None


def testGetArgumentFromCall() -> None:
    node = astroid.extract_node("foo(a, not_this_one=1, this_one=2)")
    arg = utils.get_argument_from_call(node, position=2, keyword="this_one")
    assert arg.value == 2

    node = astroid.extract_node("foo(a)")
    with pytest.raises(utils.NoSuchArgumentError):
        utils.get_argument_from_call(node, position=1)
    with pytest.raises(ValueError):
        utils.get_argument_from_call(node, None, None)
    name = utils.get_argument_from_call(node, position=0)
    assert name.name == "a"


def test_error_of_type() -> None:
    code = astroid.extract_node("""
    try: pass
    except AttributeError: #@
         pass
    try: pass
    except Exception: #@
         pass
    except: #@
         pass
    """)
    assert utils.error_of_type(code[0], AttributeError)
    assert utils.error_of_type(code[0], (AttributeError,))
    assert not utils.error_of_type(code[0], Exception)
    assert utils.error_of_type(code[1], Exception)


def test_node_ignores_exception() -> None:
    code = astroid.extract_node("""
    try:
        1/0 #@
    except ZeroDivisionError:
        pass
    try:
        1/0 #@
    except Exception:
        pass
    try:
        2/0 #@
    except:
        pass
    try:
        1/0 #@
    except ValueError:
        pass
    """)
    assert utils.node_ignores_exception(code[0], ZeroDivisionError)
    assert not utils.node_ignores_exception(code[1], ZeroDivisionError)
    assert not utils.node_ignores_exception(code[2], ZeroDivisionError)
    assert not utils.node_ignores_exception(code[3], ZeroDivisionError)


def test_is_subclass_of_node_b_derived_from_node_a() -> None:
    code = astroid.extract_node("""
    class Superclass: #@
        pass

    class Subclass(Superclass): #@
        pass
    """)
    assert utils.is_subclass_of(code[1], code[0])


def test_is_subclass_of_node_b_not_derived_from_node_a() -> None:
    code = astroid.extract_node("""
    class OneClass: #@
        pass

    class AnotherClass: #@
        pass
    """)
    assert not utils.is_subclass_of(code[1], code[0])


def test_is_subclass_of_not_classdefs() -> None:
    node = astroid.extract_node("""
    class OneClass: #@
        pass
    """)
    assert not utils.is_subclass_of(None, node)
    assert not utils.is_subclass_of(node, None)
    assert not utils.is_subclass_of(None, None)


def test_parse_format_method_string() -> None:
    samples = [
        ("{}", 1),
        ("{}:{}", 2),
        ("{field}", 1),
        ("{:5}", 1),
        ("{:10}", 1),
        ("{field:10}", 1),
        ("{field:10}{{}}", 1),
        ("{:5}{!r:10}", 2),
        ("{:5}{}{{}}{}", 3),
        ("{0}{1}{0}", 2),
        ("Coordinates: {latitude}, {longitude}", 2),
        ("X: {0[0]};  Y: {0[1]}", 1),
        ("{:*^30}", 1),
        ("{!r:}", 1),
    ]
    for fmt, count in samples:
        keys, num_args, pos_args = utils.parse_format_method_string(fmt)
        keyword_args = len({k for k, _ in keys if not isinstance(k, int)})
        assert keyword_args + num_args + pos_args == count


def test_inherit_from_std_ex_recursive_definition() -> None:
    node = astroid.extract_node("""
      import datetime
      class First(datetime.datetime):
        pass
      class Second(datetime.datetime): #@
        pass
      datetime.datetime = First
      datetime.datetime = Second
      """)
    assert not utils.inherit_from_std_ex(node)


def test_get_node_last_lineno_simple() -> None:
    node = astroid.extract_node("""
        pass
    """)
    assert utils.get_node_last_lineno(node) == 2


def test_get_node_last_lineno_if_simple() -> None:
    node = astroid.extract_node("""
        if True:
            print(1)
            pass
        """)
    assert utils.get_node_last_lineno(node) == 4


def test_get_node_last_lineno_if_elseif_else() -> None:
    node = astroid.extract_node("""
        if True:
            print(1)
        elif False:
            print(2)
        else:
            print(3)
        """)
    assert utils.get_node_last_lineno(node) == 7


def test_get_node_last_lineno_while() -> None:
    node = astroid.extract_node("""
        while True:
            print(1)
        """)
    assert utils.get_node_last_lineno(node) == 3


def test_get_node_last_lineno_while_else() -> None:
    node = astroid.extract_node("""
        while True:
            print(1)
        else:
            print(2)
        """)
    assert utils.get_node_last_lineno(node) == 5


def test_get_node_last_lineno_for() -> None:
    node = astroid.extract_node("""
        for x in range(0, 5):
            print(1)
        """)
    assert utils.get_node_last_lineno(node) == 3


def test_get_node_last_lineno_for_else() -> None:
    node = astroid.extract_node("""
        for x in range(0, 5):
            print(1)
        else:
            print(2)
        """)
    assert utils.get_node_last_lineno(node) == 5


def test_get_node_last_lineno_try() -> None:
    node = astroid.extract_node("""
        try:
            print(1)
        except ValueError:
            print(2)
        except Exception:
            print(3)
        """)
    assert utils.get_node_last_lineno(node) == 7


def test_get_node_last_lineno_try_except_else() -> None:
    node = astroid.extract_node("""
        try:
            print(1)
        except Exception:
            print(2)
            print(3)
        else:
            print(4)
        """)
    assert utils.get_node_last_lineno(node) == 8


def test_get_node_last_lineno_try_except_finally() -> None:
    node = astroid.extract_node("""
        try:
            print(1)
        except Exception:
            print(2)
        finally:
            print(4)
        """)
    assert utils.get_node_last_lineno(node) == 7


def test_get_node_last_lineno_try_except_else_finally() -> None:
    node = astroid.extract_node("""
        try:
            print(1)
        except Exception:
            print(2)
        else:
            print(3)
        finally:
            print(4)
        """)
    assert utils.get_node_last_lineno(node) == 9


def test_get_node_last_lineno_with() -> None:
    node = astroid.extract_node("""
        with x as y:
            print(1)
            pass
        """)
    assert utils.get_node_last_lineno(node) == 4


def test_get_node_last_lineno_method() -> None:
    node = astroid.extract_node("""
        def x(a, b):
            print(a, b)
            pass
        """)
    assert utils.get_node_last_lineno(node) == 4


def test_get_node_last_lineno_decorator() -> None:
    node = astroid.extract_node("""
        @decor()
        def x(a, b):
            print(a, b)
            pass
        """)
    assert utils.get_node_last_lineno(node) == 5


def test_get_node_last_lineno_class() -> None:
    node = astroid.extract_node("""
        class C(object):
            CONST = True

            def x(self, b):
                print(b)

            def y(self):
                pass
                pass
        """)
    assert utils.get_node_last_lineno(node) == 10


def test_get_node_last_lineno_combined() -> None:
    node = astroid.extract_node("""
        class C(object):
            CONST = True

            def y(self):
                try:
                    pass
                except:
                    pass
                finally:
                    pass
        """)
    assert utils.get_node_last_lineno(node) == 11


def test_is_module_member() -> None:
    """Only the asked-for member, however the module is spelled."""
    code = astroid.extract_node("""
    import os
    import sys
    import sys as system
    from sys import version_info
    from sys import version_info as vi
    from django import VERSION as version_info_of_a_library

    sys.version_info  #@
    system.version_info  #@
    version_info  #@
    vi  #@

    sys.version_info[0]  #@
    sys.version_info.major  #@
    sys.hexversion  #@
    os.version_info  #@
    version_info_of_a_library  #@
    """)
    assert isinstance(code, list) and len(code) == 9

    for spelling in code[:4]:
        assert (
            utils.is_module_member(spelling, "sys.version_info") is True
        ), spelling.as_string()

    for lookalike in code[4:]:
        assert (
            utils.is_module_member(lookalike, "sys.version_info") is False
        ), lookalike.as_string()


def test_is_module_member_several_members() -> None:
    """Any of the members asked for counts, and nothing else does."""
    code = astroid.extract_node("""
    import sys
    from sys import hexversion

    sys.version_info  #@
    sys.hexversion  #@
    hexversion  #@

    sys.maxsize  #@
    """)
    assert isinstance(code, list) and len(code) == 4

    for member in code[:3]:
        assert (
            utils.is_module_member(member, "sys.version_info", "sys.hexversion") is True
        ), member.as_string()

    assert (
        utils.is_module_member(code[3], "sys.version_info", "sys.hexversion") is False
    ), code[3].as_string()


def test_uninferable_final_decorators() -> None:
    """A `typing.final` decorator is reported only when it cannot be inferred.

    `unsupported_version` reaches for this only after `safe_infer` came up empty,
    which needs the name to have more than one possible value.
    """
    module = astroid.parse("""
    from typing import final
    if unknown_condition:
        final = something_else

    @final
    def ambiguous():
        pass

    @typing.final
    def not_even_imported():
        pass
    """)
    ambiguous, not_even_imported = module.body[-2], module.body[-1]

    assert utils.uninferable_final_decorators(ambiguous.decorators) == [
        ambiguous.decorators.nodes[0]
    ]
    assert not utils.uninferable_final_decorators(not_even_imported.decorators)


def test_is_module_member_needs_a_qualified_name() -> None:
    """A bare member name would silently match nothing, so it is refused.

    ``"version_info".rpartition(".")`` leaves an empty module name, which no
    import can bind, so the mistake has to be loud rather than a missed message.
    """
    code = astroid.extract_node("""
    import sys

    sys.version_info  #@
    """)

    with pytest.raises(ValueError, match="is not a qualified name"):
        utils.is_module_member(code, "version_info")


def test_is_module_member_aliases() -> None:
    """An alias is followed, and never taken at face value.

    What the import brings in and what it binds the result to are two different
    names, so a module or a member wearing the other one's name is not it.
    """
    code = astroid.extract_node("""
    import sys as system
    from sys import version_info as vi

    import os as sys
    import sys as version_info
    from sys import maxsize as version_info
    from os import sep as version_info

    system.version_info  #@
    vi  #@

    sys.version_info  #@
    version_info  #@
    """)
    assert isinstance(code, list) and len(code) == 4

    # `import sys as system`, then `from sys import version_info as vi`.
    assert utils.is_module_member(code[0], "sys.version_info") is True
    assert utils.is_module_member(code[1], "sys.version_info") is True

    # `sys` is really `os` here, and `version_info` is really `sys.maxsize`.
    assert utils.is_module_member(code[2], "sys.version_info") is False
    assert utils.is_module_member(code[3], "sys.version_info") is False


def test_is_module_member_dotted_module() -> None:
    """A module reached through a dotted name is resolved by inference.

    ``os.path`` is deliberately not the example: it infers to ``posixpath`` or
    to ``ntpath`` depending on the platform, so it is not its own module.
    """
    code = astroid.extract_node("""
    import xml.etree.ElementTree

    xml.etree.ElementTree.parse  #@
    xml.etree.ElementTree.does_not_matter  #@
    xml.etree.parse  #@
    """)
    assert isinstance(code, list) and len(code) == 3

    assert utils.is_module_member(code[0], "xml.etree.ElementTree.parse") is True
    # The right module, a member it does not have.
    assert utils.is_module_member(code[1], "xml.etree.ElementTree.parse") is False
    # The right member name, hanging off a different module.
    assert utils.is_module_member(code[2], "xml.etree.ElementTree.parse") is False


def test_is_module_member_shadowed_module() -> None:
    """A class named after a module reads like it and is not it."""
    code = astroid.extract_node("""
    class sys:
        version_info = (3, 12)

    sys.version_info  #@
    """)
    assert utils.is_module_member(code, "sys.version_info") is False


def test_is_module_member_import_in_a_block() -> None:
    """The import binding the module need not be at module level."""
    code = astroid.extract_node("""
    try:
        import sys
    except ImportError:
        sys = None

    sys.version_info  #@
    """)
    assert utils.is_module_member(code, "sys.version_info") is True


def test_if_sys_guard() -> None:
    code = astroid.extract_node("""
    import sys
    if sys.version_info > (3, 8):  #@
        pass

    if sys.version_info[:2] > (3, 8):  #@
        pass

    if sys.some_other_function > (3, 8):  #@
        pass

    import six
    if six.PY2:  #@
        pass

    if six.PY3:  #@
        pass

    if six.something_else:  #@
        pass
    """)
    assert isinstance(code, list) and len(code) == 6

    assert isinstance(code[0], nodes.If)
    assert utils.is_sys_guard(code[0]) is True
    assert isinstance(code[1], nodes.If)
    assert utils.is_sys_guard(code[1]) is True

    assert isinstance(code[2], nodes.If)
    assert utils.is_sys_guard(code[2]) is False

    assert isinstance(code[3], nodes.If)
    assert utils.is_sys_guard(code[3]) is True
    assert isinstance(code[4], nodes.If)
    assert utils.is_sys_guard(code[4]) is True

    assert isinstance(code[5], nodes.If)
    assert utils.is_sys_guard(code[5]) is False


def test_if_typing_guard() -> None:
    code = astroid.extract_node("""
    import typing
    import typing as t
    from typing import TYPE_CHECKING

    if typing.TYPE_CHECKING:
        pass  #@

    if t.TYPE_CHECKING:
        pass #@

    if TYPE_CHECKING:
        pass #@

    if typing.SOME_OTHER_CONST:
        pass  #@
    """)
    assert isinstance(code, list) and len(code) == 4

    assert isinstance(code[0], nodes.Pass)
    assert utils.in_type_checking_block(code[0]) is True
    assert isinstance(code[1], nodes.Pass)
    assert utils.in_type_checking_block(code[1]) is True
    assert isinstance(code[2], nodes.Pass)
    assert utils.in_type_checking_block(code[2]) is True

    assert isinstance(code[3], nodes.Pass)
    assert utils.in_type_checking_block(code[3]) is False


def test_in_type_checking_block() -> None:
    code = astroid.extract_node("""
    if TYPE_CHECKING:  # don't import this!
        import math  #@
    """)
    assert utils.in_type_checking_block(code) is False


def test_is_empty_literal() -> None:
    list_node = astroid.extract_node("a = []")
    assert utils.is_base_container(list_node.value)
    not_empty_list_node = astroid.extract_node("a = [1,2,3]")
    assert not utils.is_base_container(not_empty_list_node.value)

    tuple_node = astroid.extract_node("a = ()")
    assert utils.is_base_container(tuple_node.value)
    not_empty_tuple_node = astroid.extract_node("a = (1,2)")
    assert not utils.is_base_container(not_empty_tuple_node.value)

    dict_node = astroid.extract_node("a = {}")
    assert utils.is_empty_dict_literal(dict_node.value)
    not_empty_dict_node = astroid.extract_node("a = {1:1}")
    assert not utils.is_empty_dict_literal(not_empty_dict_node.value)

    string_node = astroid.extract_node("a = ''")
    assert utils.is_empty_str_literal(string_node.value)
    not_empty_string_node = astroid.extract_node("a = 'hello'")
    assert not utils.is_empty_str_literal(not_empty_string_node.value)


def test_is_module_member_typing() -> None:
    code = astroid.extract_node("""
    from typing import Literal as Lit, Set as Literal
    import typing as t

    Literal #@
    Lit #@
    t.Literal #@
    """)

    assert not utils.is_module_member(code[0], "typing.Literal")
    assert utils.is_module_member(code[1], "typing.Literal")
    assert utils.is_module_member(code[2], "typing.Literal")

    code = astroid.extract_node("""
    Literal #@
    typing.Literal #@
    """)
    assert not utils.is_module_member(code[0], "typing.Literal")
    assert not utils.is_module_member(code[1], "typing.Literal")


def test_is_typing_member_is_deprecated() -> None:
    """It still answers, but is_module_member is the one to call now."""
    code = astroid.extract_node("""
    from typing import Literal

    Literal #@
    """)

    with pytest.warns(DeprecationWarning, match="is_typing_member has been deprecated"):
        assert utils.is_typing_member(code, ("Literal",)) is True


def test_is_reassigned_after_current_requires_isinstance_check() -> None:
    tree = astroid.parse("""
    CONSTANT = 1

    def global_function_assign():
        global CONSTANT
        def CONSTANT():
            pass
        CONSTANT()
    """)
    func = tree.body[1]
    global_stmt = func.body[0]
    nested_func = func.body[1]

    assert isinstance(global_stmt, nodes.Global)
    assert isinstance(nested_func, nodes.FunctionDef)

    node_scope = global_stmt.scope()

    assert nested_func.scope() == nested_func
    assert nested_func.scope() != node_scope

    assert nested_func.parent.scope() == node_scope

    assert utils.is_reassigned_after_current(global_stmt, "CONSTANT") is True


def test_is_reassigned_before_current() -> None:
    tree = astroid.parse("""
    x = 1
    x = 2
    x = 3
    """)
    first_assign = tree.body[0]
    second_assign = tree.body[1]
    third_assign = tree.body[2]

    assert isinstance(first_assign, nodes.Assign)
    assert isinstance(second_assign, nodes.Assign)
    assert isinstance(third_assign, nodes.Assign)

    third_assign_name = third_assign.targets[0]
    first_assign_name = first_assign.targets[0]

    assert isinstance(third_assign_name, nodes.AssignName)
    assert isinstance(first_assign_name, nodes.AssignName)

    assert utils.is_reassigned_before_current(third_assign_name, "x") is True
    assert utils.is_reassigned_before_current(first_assign_name, "x") is False


def test_is_reassigned_after_current_with_assignname() -> None:
    tree = astroid.parse("""
    x = 1
    x = 2
    x = 3
    """)
    first_assign = tree.body[0]
    second_assign = tree.body[1]
    third_assign = tree.body[2]

    assert isinstance(first_assign, nodes.Assign)
    assert isinstance(second_assign, nodes.Assign)
    assert isinstance(third_assign, nodes.Assign)

    first_assign_name = first_assign.targets[0]
    third_assign_name = third_assign.targets[0]

    assert isinstance(first_assign_name, nodes.AssignName)
    assert isinstance(third_assign_name, nodes.AssignName)

    assert utils.is_reassigned_after_current(first_assign_name, "x") is True
    assert utils.is_reassigned_after_current(third_assign_name, "x") is False


def test_is_reassigned_with_node_no_lineno() -> None:
    tree = astroid.parse("""
    x = 1
    x = 2
    """)
    first_assign = tree.body[0]
    first_assign_name = first_assign.targets[0]

    assert isinstance(first_assign_name, nodes.AssignName)
    original_lineno = first_assign_name.lineno
    first_assign_name.lineno = None

    try:
        assert utils.is_reassigned_after_current(first_assign_name, "x") is False
        assert utils.is_reassigned_before_current(first_assign_name, "x") is False
    finally:
        first_assign_name.lineno = original_lineno


def test_is_terminating_func_unittest_fail() -> None:
    node = astroid.extract_node("""
    from unittest import TestCase
    import os

    class TestX(TestCase):
        def test_foo(self):
            if 'FOO' in os.environ:
                x = 1
            else:
                self.fail()  #@
            print(x)
    """)
    result = utils.is_terminating_func(node)
    assert result is True


def test_is_terminating_func_ignored_overload_noreturn() -> None:
    node = astroid.extract_node("""
    from typing import Literal, NoReturn, overload
    @overload
    def create_client(version: int = ...) -> NoReturn: ...
    @overload
    def create_client(version: Literal[2] = ...) -> int: ...
    def create_client(version: int = 2) -> int:
        return 1
    create_client(version=2)  #@
    """)
    result = utils.is_terminating_func(node)
    assert result is False


def test_is_terminating_func_overload_with_noreturn_implementation() -> None:
    node = astroid.extract_node("""
    from typing import NoReturn, overload

    @overload
    def always_fails(code: int) -> NoReturn: ...
    @overload
    def always_fails(code: str) -> NoReturn: ...

    def always_fails(code: int | str) -> NoReturn:
        raise SystemExit(code)

    always_fails(1)  #@
""")
    result = utils.is_terminating_func(node)
    assert result is True
