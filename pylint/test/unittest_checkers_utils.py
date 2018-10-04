# Copyright (c) 2010 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2013-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Caio Carrara <ccarrara@redhat.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the pylint.checkers.utils module."""

import astroid

from pylint.checkers import utils
import pytest


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
    assert 2 == arg.value

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
    assert utils.error_of_type(nodes[2], ImportError)


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
    assert utils.node_ignores_exception(nodes[2], ZeroDivisionError)
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
        keyword_args = len(set(k for k, l in keys if not isinstance(k, int)))
        assert keyword_args + num_args + pos_args == count
