# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the pylint.checkers.utils module."""

from __future__ import annotations

import astroid
import pytest
from astroid import nodes

from pylint.checkers import utils
from pylint.checkers.utils import (  # pylint: disable=no-name-in-module
    parse_format_method_string_result,
)


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
    result_type = parse_format_method_string_result
    samples = [
        ("{}", result_type([], 1, {}, {}, [(None, None)], {})),
        ("{}:{}", result_type([], 2, {}, {}, [(None, None), (None, None)], {})),
        (
            "{field}",
            result_type([("field", [])], 0, {}, {"field": (None, None)}, [], {}),
        ),
        ("{:5}", result_type([], 1, {}, {}, [(None, None)], {})),
        ("{:10}", result_type([], 1, {}, {}, [(None, None)], {})),
        (
            "{field:10}",
            result_type([("field", [])], 0, {}, {"field": (None, None)}, [], {}),
        ),
        (
            "{field:10}{{}}",
            result_type([("field", [])], 0, {}, {"field": (None, None)}, [], {}),
        ),
        ("{:5}{!r:10}", result_type([], 2, {}, {}, [(None, None), ("r", None)], {})),
        (
            "{:5}{}{{}}{}",
            result_type([], 3, {}, {}, [(None, None), (None, None), (None, None)], {}),
        ),
        (
            "{0}{1}{0}",
            result_type(
                [],
                0,
                {"0": [], "1": []},
                {},
                [],
                {"0": (None, None), "1": (None, None)},
            ),
        ),
        (
            "Coordinates: {latitude}, {longitude}",
            result_type(
                [("latitude", []), ("longitude", [])],
                0,
                {},
                {"latitude": (None, None), "longitude": (None, None)},
                [],
                {},
            ),
        ),
        (
            "X: {0[0]};  Y: {0[1]}",
            result_type([], 0, {"0": [(False, 1)]}, {}, [], {"0": (None, None)}),
        ),
        ("{:*^30}", result_type([], 1, {}, {}, [(None, None)], {})),
        ("{!r:}", result_type([], 1, {}, {}, [("r", None)], {})),
        (
            "{0.missing}",
            result_type([], 0, {"0": [(True, "missing")]}, {}, [], {"0": (None, None)}),
        ),
    ]
    for fmt, expected in samples:
        assert utils.parse_format_method_string(fmt) == expected


@pytest.mark.parametrize(
    "spec,expected",
    [
        ("", None),
        ("d", "d"),
        ("x", "x"),
        ("X", "X"),
        ("o", "o"),
        ("b", "b"),
        ("f", "f"),
        ("F", "F"),
        ("e", "e"),
        ("E", "E"),
        ("g", "g"),
        ("G", "G"),
        ("n", "n"),
        ("s", "s"),
        ("c", "c"),
        # Any spec containing ``%`` is treated as a strftime-style pattern
        # and short-circuits to ``None`` (no format char to validate);
        # ``"%"`` alone is in that class even though it's also a valid
        # builtin format character on its own.
        ("%", None),
        # Common variants: width, precision, alignment, sign, padding.
        (".2f", "f"),
        ("02d", "d"),
        (">10s", "s"),
        ("+d", "d"),
        ("#x", "x"),
        ("_d", "d"),
        (",.2f", "f"),
        # A spec containing ``%`` is treated as a strftime-style pattern; no
        # format char to validate.
        ("%Y-%m-%d", None),
        # A nested replacement field ``{...}`` may appear in the spec for
        # dynamic precision / width; the regex allows it.
        ("{}d", "d"),
        ("{0}d", "d"),
    ],
)
def test_parse_format_spec_valid(spec: str, expected: str | None) -> None:
    assert utils.parse_format_spec(spec, 0) == expected


def test_parse_format_spec_unsupported_char() -> None:
    with pytest.raises(utils.UnsupportedFormatCharacter) as exc:
        utils.parse_format_spec("p", 0)
    assert exc.value.index == 0
    with pytest.raises(utils.UnsupportedFormatCharacter) as exc:
        utils.parse_format_spec(".2v", 5)
    # 5 (start) + position of "v" within ".2v" (i.e. 2)
    assert exc.value.index == 7


def test_parse_format_spec_incomplete() -> None:
    # "foo" doesn't match the mini-format-spec grammar at all.
    with pytest.raises(utils.IncompleteFormatString):
        utils.parse_format_spec("foo", 0)
    with pytest.raises(utils.IncompleteFormatString):
        utils.parse_format_spec("latex", 0)


@pytest.mark.parametrize(
    "field,expected",
    [
        # name, no spec, no conversion
        ("x", ("", (None, None))),
        # name + spec
        ("x:d", ("d", (None, "d"))),
        ("x:.2f", (".2f", (None, "f"))),
        # name + conversion
        ("x!r", ("", ("r", None))),
        ("x!s:d", ("d", ("s", "d"))),
        # indexed / attribute access
        ("0", ("", (None, None))),
        ("0[1]:d", ("d", (None, "d"))),
        # bracket-aware: ``:`` inside brackets is not the spec separator
        ("a[b:c]", ("", (None, None))),
        # quoted bracket key
        ("a['b:c']", ("", (None, None))),
    ],
)
def test_parse_format_field(field: str, expected: tuple) -> None:
    assert utils.parse_format_field(field, 0) == expected


def test_parse_format_field_unbalanced_bracket() -> None:
    with pytest.raises(utils.IncompleteFormatString):
        utils.parse_format_field("a]", 0)


def test_parse_format_field_bad_conversion() -> None:
    # Only ``r``, ``s``, ``a`` (in callers; here ``r``/``s``) are valid;
    # ``z`` is bogus.
    with pytest.raises(utils.UnsupportedFormatCharacter):
        utils.parse_format_field("x!z", 0)


@pytest.mark.parametrize(
    "field",
    [
        # A balanced "..." inside brackets is fine; the close pops the open.
        'a["b"]',
        # A balanced \'...\' inside brackets is fine.
        "a['b']",
    ],
)
def test_parse_format_field_balanced_quotes(field: str) -> None:
    # No exception: the open/close pair balances cleanly.
    assert utils.parse_format_field(field, 0) == ("", (None, None))


def test_parse_format_field_unbalanced_double_quote() -> None:
    # ``a["b"c"d]`` re-opens ``"`` after a closing one inside brackets;
    # parse_format_field detects the second ``"`` while the bracket is
    # still open and raises.
    with pytest.raises(utils.IncompleteFormatString):
        utils.parse_format_field('a["b"c"d]', 0)


def test_parse_format_field_unbalanced_single_quote() -> None:
    with pytest.raises(utils.IncompleteFormatString):
        utils.parse_format_field("a['b'c'd]", 0)


def test_parse_format_field_double_quote_already_open() -> None:
    # Field text: ``'a'"b'c"`` (note: outer single-quoted Python literal so
    # we have ``'``...``"``...``'``...``"``). When we hit the second ``"``
    # at the end, the open_blocks stack is [``"``, ``'``]; the ``"`` is
    # already in the stack but not at the top -> IncompleteFormatString.
    with pytest.raises(utils.IncompleteFormatString):
        utils.parse_format_field("'a'\"b'c\"", 0)


def test_parse_format_field_single_quote_already_open() -> None:
    # Mirror of the above for the single-quote branch:
    # ``"a"'b"'`` ends with open_blocks=[``'``, ``"``] and ``'`` is already
    # present below the top -> IncompleteFormatString.
    with pytest.raises(utils.IncompleteFormatString):
        utils.parse_format_field('"a"\'b"\'', 0)


@pytest.mark.parametrize(
    "fmt,expected_keys",
    [
        ("{}", {""}),
        ("{:d}", {"d"}),
        ("{x:d}", {"d"}),
        ("{} {}", {""}),
        ("{:d} {:s}", {"d", "s"}),
        # {{ and }} are literal braces, not field delimiters
        ("{{}}", set()),
        ("hello {x}", {""}),
        # Nested replacement fields in the spec
        ("{x:{y}}", {"{y}", ""}),
    ],
)
def test_parse_all_fields_formatting(fmt: str, expected_keys: set) -> None:
    result = utils.parse_all_fields_formatting(fmt, include_nested=True)
    assert set(result) == expected_keys


def test_parse_all_fields_formatting_unbalanced() -> None:
    # Stray ``}`` with no opener.
    with pytest.raises(utils.IncompleteFormatString):
        utils.parse_all_fields_formatting("}", include_nested=True)
    # Unclosed ``{``.
    with pytest.raises(utils.IncompleteFormatString):
        utils.parse_all_fields_formatting("{x", include_nested=True)


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


def test_is_typing_member() -> None:
    code = astroid.extract_node("""
    from typing import Literal as Lit, Set as Literal
    import typing as t

    Literal #@
    Lit #@
    t.Literal #@
    """)

    assert not utils.is_typing_member(code[0], ("Literal",))
    assert utils.is_typing_member(code[1], ("Literal",))
    assert utils.is_typing_member(code[2], ("Literal",))

    code = astroid.extract_node("""
    Literal #@
    typing.Literal #@
    """)
    assert not utils.is_typing_member(code[0], ("Literal",))
    assert not utils.is_typing_member(code[1], ("Literal",))


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
