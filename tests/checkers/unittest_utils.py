# Copyright (c) 2010 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2013-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Alan Chan <achan961117@gmail.com>
# Copyright (c) 2018 Caio Carrara <ccarrara@redhat.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2019 Nathan Marrow <nmarrow@google.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Tests for the pylint.checkers.utils module."""

import astroid
import pytest

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
def testIsBuiltin(name, expected):
    assert utils.is_builtin(name) == expected


@pytest.mark.parametrize(
    "fn,kw",
    [("foo(3)", {"keyword": "bar"}), ("foo(one=a, two=b, three=c)", {"position": 1})],
)
def testGetArgumentFromCallError(fn, kw):
    with pytest.raises(utils.NoSuchArgumentError):
        node = astroid.extract_node(fn)
        utils.get_argument_from_call(node, **kw)


@pytest.mark.parametrize(
    "fn,kw", [("foo(bar=3)", {"keyword": "bar"}), ("foo(a, b, c)", {"position": 1})]
)
def testGetArgumentFromCallExists(fn, kw):
    node = astroid.extract_node(fn)
    assert utils.get_argument_from_call(node, **kw) is not None


def testGetArgumentFromCall():
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


def test_error_of_type():
    nodes = astroid.extract_node(
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
    assert utils.error_of_type(nodes[0], AttributeError)
    assert utils.error_of_type(nodes[0], (AttributeError,))
    assert not utils.error_of_type(nodes[0], Exception)
    assert utils.error_of_type(nodes[1], Exception)


def test_node_ignores_exception():
    nodes = astroid.extract_node(
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
    assert utils.node_ignores_exception(nodes[0], ZeroDivisionError)
    assert not utils.node_ignores_exception(nodes[1], ZeroDivisionError)
    assert not utils.node_ignores_exception(nodes[2], ZeroDivisionError)
    assert not utils.node_ignores_exception(nodes[3], ZeroDivisionError)


def test_is_subclass_of_node_b_derived_from_node_a():
    nodes = astroid.extract_node(
        """
    class Superclass: #@
        pass

    class Subclass(Superclass): #@
        pass
    """
    )
    assert utils.is_subclass_of(nodes[1], nodes[0])


def test_is_subclass_of_node_b_not_derived_from_node_a():
    nodes = astroid.extract_node(
        """
    class OneClass: #@
        pass

    class AnotherClass: #@
        pass
    """
    )
    assert not utils.is_subclass_of(nodes[1], nodes[0])


def test_is_subclass_of_not_classdefs():
    node = astroid.extract_node(
        """
    class OneClass: #@
        pass
    """
    )
    assert not utils.is_subclass_of(None, node)
    assert not utils.is_subclass_of(node, None)
    assert not utils.is_subclass_of(None, None)


def test_parse_format_method_string():
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
        keyword_args = len({k for k, l in keys if not isinstance(k, int)})
        assert keyword_args + num_args + pos_args == count


def test_inherit_from_std_ex_recursive_definition():
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


def test_get_node_last_lineno_simple():
    node = astroid.extract_node(
        """
        pass
    """
    )
    assert utils.get_node_last_lineno(node) == 2


def test_get_node_last_lineno_if_simple():
    node = astroid.extract_node(
        """
        if True:
            print(1)
            pass
        """
    )
    assert utils.get_node_last_lineno(node) == 4


def test_get_node_last_lineno_if_elseif_else():
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


def test_get_node_last_lineno_while():
    node = astroid.extract_node(
        """
        while True:
            print(1)
        """
    )
    assert utils.get_node_last_lineno(node) == 3


def test_get_node_last_lineno_while_else():
    node = astroid.extract_node(
        """
        while True:
            print(1)
        else:
            print(2)
        """
    )
    assert utils.get_node_last_lineno(node) == 5


def test_get_node_last_lineno_for():
    node = astroid.extract_node(
        """
        for x in range(0, 5):
            print(1)
        """
    )
    assert utils.get_node_last_lineno(node) == 3


def test_get_node_last_lineno_for_else():
    node = astroid.extract_node(
        """
        for x in range(0, 5):
            print(1)
        else:
            print(2)
        """
    )
    assert utils.get_node_last_lineno(node) == 5


def test_get_node_last_lineno_try():
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


def test_get_node_last_lineno_try_except_else():
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


def test_get_node_last_lineno_try_except_finally():
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


def test_get_node_last_lineno_try_except_else_finally():
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


def test_get_node_last_lineno_with():
    node = astroid.extract_node(
        """
        with x as y:
            print(1)
            pass
        """
    )
    assert utils.get_node_last_lineno(node) == 4


def test_get_node_last_lineno_method():
    node = astroid.extract_node(
        """
        def x(a, b):
            print(a, b)
            pass
        """
    )
    assert utils.get_node_last_lineno(node) == 4


def test_get_node_last_lineno_decorator():
    node = astroid.extract_node(
        """
        @decor()
        def x(a, b):
            print(a, b)
            pass
        """
    )
    assert utils.get_node_last_lineno(node) == 5


def test_get_node_last_lineno_class():
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


def test_get_node_last_lineno_combined():
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


class TestStatementsAreExclusive:
    @staticmethod
    @pytest.mark.parametrize(
        "first, second, expected_result",
        [
            pytest.param(0, 1, False, id="not-under-common-ifelse"),
            pytest.param(1, 2, True, id="if-and-else"),
            pytest.param(2, 1, True, id="if-and-else-swapped"),
            pytest.param(2, 3, False, id="both-in-else"),
        ],
    )
    def test_if_else(first, second, expected_result):
        nodes = astroid.extract_node(
            """
            print("Test")  #@
            if condition:
                print("condition is True")  #@
            else:
                print("condition is False")  #@
                print("condition really is False")  #@
            """
        )
        assert (
            utils.statements_are_exclusive(nodes[first], nodes[second])
            is expected_result
        )

    @staticmethod
    def test_if_exp():
        node = astroid.extract_node("res = 1 if predicate else 2  #@")
        first = node.value.body
        second = node.value.orelse
        assert utils.statements_are_exclusive(first, second) is True

    @staticmethod
    @pytest.mark.parametrize(
        "first, second, expected_result",
        [
            pytest.param(0, 1, False, id="both-in-try"),
            pytest.param(1, 2, True, id="try-and-except"),
            pytest.param(1, 4, False, id="try-and-else"),
            pytest.param(2, 3, True, id="different-excepts"),
            pytest.param(3, 4, True, id="except-and-else"),
            pytest.param(1, 5, True, id="try-and-finally"),
            pytest.param(3, 5, True, id="except-and-finally"),
            pytest.param(1, 6, False, id="not-under-common-tryexcept"),
        ],
    )
    def test_try_except(first, second, expected_result):
        """
        The control flow inside a try-except-finally is a bit tricky, so we make
        some assumptions to simplify things:
        1. As the ``try`` block could be interrupted at any time, we assume that the body
           of the ``try`` and the body of the exception handlers are always exclusive.
        2. Different exception handlers are seen as exclusive
        3. try/except bodies and the body of a ``finally`` are seen as exclusive
        What can never be exclusive is the body of the ``try`` and (if existant) the content
        of the ``else`` block, as the else block is only reached if the ``try`` finished without
        exception.
        """
        nodes = astroid.extract_node(
            """
            try:
                enter_shop()  #@
                buy_a_horse()  #@
            except OutOfHorses:
                say("damn it!")  #@
            except NotEnoughMoney:
                buy_a_pig_instead()  #@
            else:
                say("Now let's get some hay.")  #@
            finally:
                leave_shop()  #@
            say("Let's go home")  #@
            """
        )
        assert (
            utils.statements_are_exclusive(nodes[first], nodes[second])
            is expected_result
        )
