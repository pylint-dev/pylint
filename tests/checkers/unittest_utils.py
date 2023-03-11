# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

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
    code = astroid.extract_node(
        """
    try: pass
    except AttributeError: #@
         pass
    try: pass
    except Exception: #@
         pass
    except: #@
         pass
    """
    )
    assert utils.error_of_type(code[0], AttributeError)
    assert utils.error_of_type(code[0], (AttributeError,))
    assert not utils.error_of_type(code[0], Exception)
    assert utils.error_of_type(code[1], Exception)


def test_node_ignores_exception() -> None:
    code = astroid.extract_node(
        """
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
    """
    )
    assert utils.node_ignores_exception(code[0], ZeroDivisionError)
    assert not utils.node_ignores_exception(code[1], ZeroDivisionError)
    assert not utils.node_ignores_exception(code[2], ZeroDivisionError)
    assert not utils.node_ignores_exception(code[3], ZeroDivisionError)


def test_is_subclass_of_node_b_derived_from_node_a() -> None:
    code = astroid.extract_node(
        """
    class Superclass: #@
        pass

    class Subclass(Superclass): #@
        pass
    """
    )
    assert utils.is_subclass_of(code[1], code[0])


def test_is_subclass_of_node_b_not_derived_from_node_a() -> None:
    code = astroid.extract_node(
        """
    class OneClass: #@
        pass

    class AnotherClass: #@
        pass
    """
    )
    assert not utils.is_subclass_of(code[1], code[0])


def test_is_subclass_of_not_classdefs() -> None:
    node = astroid.extract_node(
        """
    class OneClass: #@
        pass
    """
    )
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
    node = astroid.extract_node(
        """
      import datetime
      class First(datetime.datetime):
        pass
      class Second(datetime.datetime): #@
        pass
      datetime.datetime = First
      datetime.datetime = Second
      """
    )
    assert not utils.inherit_from_std_ex(node)


def test_get_node_last_lineno_simple() -> None:
    node = astroid.extract_node(
        """
        pass
    """
    )
    assert utils.get_node_last_lineno(node) == 2


def test_get_node_last_lineno_if_simple() -> None:
    node = astroid.extract_node(
        """
        if True:
            print(1)
            pass
        """
    )
    assert utils.get_node_last_lineno(node) == 4


def test_get_node_last_lineno_if_elseif_else() -> None:
    node = astroid.extract_node(
        """
        if True:
            print(1)
        elif False:
            print(2)
        else:
            print(3)
        """
    )
    assert utils.get_node_last_lineno(node) == 7


def test_get_node_last_lineno_while() -> None:
    node = astroid.extract_node(
        """
        while True:
            print(1)
        """
    )
    assert utils.get_node_last_lineno(node) == 3


def test_get_node_last_lineno_while_else() -> None:
    node = astroid.extract_node(
        """
        while True:
            print(1)
        else:
            print(2)
        """
    )
    assert utils.get_node_last_lineno(node) == 5


def test_get_node_last_lineno_for() -> None:
    node = astroid.extract_node(
        """
        for x in range(0, 5):
            print(1)
        """
    )
    assert utils.get_node_last_lineno(node) == 3


def test_get_node_last_lineno_for_else() -> None:
    node = astroid.extract_node(
        """
        for x in range(0, 5):
            print(1)
        else:
            print(2)
        """
    )
    assert utils.get_node_last_lineno(node) == 5


def test_get_node_last_lineno_try() -> None:
    node = astroid.extract_node(
        """
        try:
            print(1)
        except ValueError:
            print(2)
        except Exception:
            print(3)
        """
    )
    assert utils.get_node_last_lineno(node) == 7


def test_get_node_last_lineno_try_except_else() -> None:
    node = astroid.extract_node(
        """
        try:
            print(1)
        except Exception:
            print(2)
            print(3)
        else:
            print(4)
        """
    )
    assert utils.get_node_last_lineno(node) == 8


def test_get_node_last_lineno_try_except_finally() -> None:
    node = astroid.extract_node(
        """
        try:
            print(1)
        except Exception:
            print(2)
        finally:
            print(4)
        """
    )
    assert utils.get_node_last_lineno(node) == 7


def test_get_node_last_lineno_try_except_else_finally() -> None:
    node = astroid.extract_node(
        """
        try:
            print(1)
        except Exception:
            print(2)
        else:
            print(3)
        finally:
            print(4)
        """
    )
    assert utils.get_node_last_lineno(node) == 9


def test_get_node_last_lineno_with() -> None:
    node = astroid.extract_node(
        """
        with x as y:
            print(1)
            pass
        """
    )
    assert utils.get_node_last_lineno(node) == 4


def test_get_node_last_lineno_method() -> None:
    node = astroid.extract_node(
        """
        def x(a, b):
            print(a, b)
            pass
        """
    )
    assert utils.get_node_last_lineno(node) == 4


def test_get_node_last_lineno_decorator() -> None:
    node = astroid.extract_node(
        """
        @decor()
        def x(a, b):
            print(a, b)
            pass
        """
    )
    assert utils.get_node_last_lineno(node) == 5


def test_get_node_last_lineno_class() -> None:
    node = astroid.extract_node(
        """
        class C(object):
            CONST = True

            def x(self, b):
                print(b)

            def y(self):
                pass
                pass
        """
    )
    assert utils.get_node_last_lineno(node) == 10


def test_get_node_last_lineno_combined() -> None:
    node = astroid.extract_node(
        """
        class C(object):
            CONST = True

            def y(self):
                try:
                    pass
                except:
                    pass
                finally:
                    pass
        """
    )
    assert utils.get_node_last_lineno(node) == 11


def test_if_sys_guard() -> None:
    code = astroid.extract_node(
        """
    import sys
    if sys.version_info > (3, 8):  #@
        pass

    if sys.version_info[:2] > (3, 8):  #@
        pass

    if sys.some_other_function > (3, 8):  #@
        pass
    """
    )
    assert isinstance(code, list) and len(code) == 3

    assert isinstance(code[0], nodes.If)
    assert utils.is_sys_guard(code[0]) is True
    assert isinstance(code[1], nodes.If)
    assert utils.is_sys_guard(code[1]) is True

    assert isinstance(code[2], nodes.If)
    assert utils.is_sys_guard(code[2]) is False


def test_if_typing_guard() -> None:
    code = astroid.extract_node(
        """
    import typing
    import typing as t
    from typing import TYPE_CHECKING

    if typing.TYPE_CHECKING:  #@
        pass

    if t.TYPE_CHECKING:  #@
        pass

    if TYPE_CHECKING:  #@
        pass

    if typing.SOME_OTHER_CONST:  #@
        pass
    """
    )
    assert isinstance(code, list) and len(code) == 4

    assert isinstance(code[0], nodes.If)
    assert utils.is_typing_guard(code[0]) is True
    assert isinstance(code[1], nodes.If)
    assert utils.is_typing_guard(code[1]) is True
    assert isinstance(code[2], nodes.If)
    assert utils.is_typing_guard(code[2]) is True

    assert isinstance(code[3], nodes.If)
    assert utils.is_typing_guard(code[3]) is False


def test_in_type_checking_block() -> None:
    code = astroid.extract_node(
        """
    if TYPE_CHECKING:  # don't import this!
        import math  #@
    """
    )
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
    code = astroid.extract_node(
        """
    from typing import Literal as Lit, Set as Literal
    import typing as t

    Literal #@
    Lit #@
    t.Literal #@
    """
    )

    assert not utils.is_typing_member(code[0], ("Literal",))
    assert utils.is_typing_member(code[1], ("Literal",))
    assert utils.is_typing_member(code[2], ("Literal",))

    code = astroid.extract_node(
        """
    Literal #@
    typing.Literal #@
    """
    )
    assert not utils.is_typing_member(code[0], ("Literal",))
    assert not utils.is_typing_member(code[1], ("Literal",))
