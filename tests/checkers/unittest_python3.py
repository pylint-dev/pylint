# Copyright (c) 2014-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014-2015 Brett Cannon <brett@python.org>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2015 Cosmin Poieana <cmin@ropython.org>
# Copyright (c) 2015 Viorel Stirbu <viorels@gmail.com>
# Copyright (c) 2016-2017 Roy Williams <roy.williams.iii@gmail.com>
# Copyright (c) 2016 Roy Williams <rwilliams@lyft.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2017 Daniel Miller <millerdev@gmail.com>
# Copyright (c) 2018-2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2018 sbagan <pnlbagan@gmail.com>
# Copyright (c) 2018 Aivar Annamaa <aivarannamaa@users.noreply.github.com>
# Copyright (c) 2018 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Gabriel R Sezefredo <gabriel@sezefredo.com.br>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Federico Bond <federicobond@gmail.com>
# Copyright (c) 2020 Athos Ribeiro <athoscr@fedoraproject.org>
# Copyright (c) 2021 Tiago Honorato <tiagohonorato1@gmail.com>
# Copyright (c) 2021 tiagohonorato <61059243+tiagohonorato@users.noreply.github.com>
# Copyright (c) 2021 David Gilman <davidgilman1@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Tests for the python3 checkers."""

# pylint: disable=too-many-public-methods,redefined-outer-name

import astroid

from pylint import testutils
from pylint.checkers import python3 as checker
from pylint.interfaces import INFERENCE, INFERENCE_FAILURE

# TODO(cpopa): Port these to the functional test framework instead. pylint: disable=fixme


class TestPython3Checker(testutils.CheckerTestCase):

    CHECKER_CLASS = checker.Python3Checker

    def check_bad_builtin(self, builtin_name):
        node = astroid.extract_node(builtin_name + "  #@")
        message = builtin_name.lower() + "-builtin"
        with self.assertAddsMessages(testutils.Message(message, node=node)):
            self.checker.visit_name(node)

    def test_bad_builtins(self):
        builtins = [
            "apply",
            "buffer",
            "cmp",
            "coerce",
            "execfile",
            "file",
            "input",
            "intern",
            "long",
            "raw_input",
            "round",
            "reduce",
            "StandardError",
            "unichr",
            "unicode",
            "xrange",
            "reload",
        ]
        for builtin in builtins:
            self.check_bad_builtin(builtin)

    def as_iterable_in_for_loop_test(self, fxn):
        code = f"for x in {fxn}(): pass"
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_used_by_iterable_in_for_loop_test(self, fxn):
        checker = f"{fxn}-builtin-not-iterating"
        node = astroid.extract_node(
            f"""
        for x in (whatever(
            {fxn}() #@
        )):
            pass
        """
        )
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_iterable_in_genexp_test(self, fxn):
        code = f"x = (x for x in {fxn}())"
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_iterable_in_starred_context(self, fxn):
        code = f"x = test(*{fxn}())"
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_iterable_in_listcomp_test(self, fxn):
        code = f"x = [x for x in {fxn}(None, [1])]"
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_iterable_in_yield_from(self, fxn):
        code = f"yield from {fxn}()"
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_used_in_variant_in_genexp_test(self, fxn):
        checker = f"{fxn}-builtin-not-iterating"
        node = astroid.extract_node(
            f"""
        list(
            __({fxn}(x))
            for x in [1]
        )
        """
        )
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_used_in_variant_in_listcomp_test(self, fxn):
        checker = f"{fxn}-builtin-not-iterating"
        node = astroid.extract_node(
            f"""
        [
            __({fxn}(None, x))
        for x in [[1]]]
        """
        )
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_argument_to_callable_constructor_test(self, fxn, callable_fn):
        module = astroid.parse(f"x = {callable_fn}({fxn}())")
        with self.assertNoMessages():
            self.walk(module)

    def as_argument_to_materialized_filter(self, callable_fn):
        module = astroid.parse(f"list(filter(None, {callable_fn}()))")
        with self.assertNoMessages():
            self.walk(module)

    def as_argument_to_random_fxn_test(self, fxn):
        checker = f"{fxn}-builtin-not-iterating"
        node = astroid.extract_node(
            f"""
        y(
            {fxn}() #@
        )
        """
        )
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_argument_to_str_join_test(self, fxn):
        code = f"x = ''.join({fxn}())"
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_argument_to_itertools_functions(self, fxn):
        code = f"""
        from __future__ import absolute_import
        import itertools
        from itertools import product
        for i,j in product({fxn}(), repeat=2):
            pass
        for i,j in itertools.product({fxn}(), repeat=2):
            pass
        """
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_argument_to_zip_test(self, fxn):
        module = astroid.parse(f"list(zip({fxn}))")
        with self.assertNoMessages():
            self.walk(module)

    def as_argument_to_map_test(self, fxn):
        module = astroid.parse(f"list(map(__, {fxn}()))")
        with self.assertNoMessages():
            self.walk(module)

    def as_iterable_in_unpacking(self, fxn):
        node = astroid.extract_node(
            f"""
        a, b = __({fxn}())
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def as_assignment(self, fxn):
        checker = f"{fxn}-builtin-not-iterating"
        node = astroid.extract_node(
            f"""
        a = __({fxn}())
        """
        )
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def iterating_context_tests(self, fxn):
        """Helper for verifying a function isn't used as an iterator."""
        self.as_iterable_in_for_loop_test(fxn)
        self.as_used_by_iterable_in_for_loop_test(fxn)
        self.as_iterable_in_genexp_test(fxn)
        self.as_iterable_in_listcomp_test(fxn)
        self.as_used_in_variant_in_genexp_test(fxn)
        self.as_used_in_variant_in_listcomp_test(fxn)
        self.as_argument_to_random_fxn_test(fxn)
        self.as_argument_to_str_join_test(fxn)
        self.as_iterable_in_unpacking(fxn)
        self.as_assignment(fxn)
        self.as_argument_to_materialized_filter(fxn)
        self.as_iterable_in_yield_from(fxn)
        self.as_iterable_in_starred_context(fxn)
        self.as_argument_to_itertools_functions(fxn)
        self.as_argument_to_zip_test(fxn)
        self.as_argument_to_map_test(fxn)
        for func in (
            "iter",
            "list",
            "tuple",
            "sorted",
            "set",
            "sum",
            "any",
            "all",
            "enumerate",
            "dict",
            "OrderedDict",
        ):
            self.as_argument_to_callable_constructor_test(fxn, func)

    def test_dict_subclasses_methods_in_iterating_context(self):
        iterating, not_iterating = astroid.extract_node(
            """
        from __future__ import absolute_import
        from collections import defaultdict
        d = defaultdict(list)
        a, b = d.keys() #@
        x = d.keys() #@
        """
        )

        with self.assertNoMessages():
            self.checker.visit_call(iterating.value)

        message = testutils.Message("dict-keys-not-iterating", node=not_iterating.value)
        with self.assertAddsMessages(message):
            self.checker.visit_call(not_iterating.value)

    def test_dict_methods_in_iterating_context(self):
        iterating_code = [
            "for x in {}(): pass",
            "(x for x in {}())",
            "[x for x in {}()]",
            "iter({}())",
            "a, b = {}()",
            "max({}())",
            "min({}())",
            "3 in {}()",
            "3 not in {}()",
            "set().update({}())",
            "[].extend({}())",
            "{{}}.update({}())",
            """
            from __future__ import absolute_import
            from itertools import chain
            chain.from_iterable({}())
            """,
        ]
        non_iterating_code = ["x = __({}())", "__({}())[0]"]

        for method in ("keys", "items", "values"):
            dict_method = f"{{}}.{method}"

            for code in iterating_code:
                with_value = code.format(dict_method)
                module = astroid.parse(with_value)
                with self.assertNoMessages():
                    self.walk(module)

            for code in non_iterating_code:
                with_value = code.format(dict_method)
                node = astroid.extract_node(with_value)

                checker = f"dict-{method}-not-iterating"
                message = testutils.Message(checker, node=node)
                with self.assertAddsMessages(message):
                    self.checker.visit_call(node)

    def test_map_in_iterating_context(self):
        self.iterating_context_tests("map")

    def test_zip_in_iterating_context(self):
        self.iterating_context_tests("zip")

    def test_range_in_iterating_context(self):
        self.iterating_context_tests("range")

    def test_filter_in_iterating_context(self):
        self.iterating_context_tests("filter")

    def defined_method_test(self, method, warning):
        """Helper for verifying that a certain method is not defined."""
        node = astroid.extract_node(
            f"""
            class Foo(object):
                def __{method}__(self, other):  #@
                    pass"""
        )
        message = testutils.Message(warning, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(node)

    def test_delslice_method(self):
        self.defined_method_test("delslice", "delslice-method")

    def test_getslice_method(self):
        self.defined_method_test("getslice", "getslice-method")

    def test_setslice_method(self):
        self.defined_method_test("setslice", "setslice-method")

    def test_coerce_method(self):
        self.defined_method_test("coerce", "coerce-method")

    def test_oct_method(self):
        self.defined_method_test("oct", "oct-method")

    def test_hex_method(self):
        self.defined_method_test("hex", "hex-method")

    def test_nonzero_method(self):
        self.defined_method_test("nonzero", "nonzero-method")

    def test_cmp_method(self):
        self.defined_method_test("cmp", "cmp-method")

    def test_div_method(self):
        self.defined_method_test("div", "div-method")

    def test_idiv_method(self):
        self.defined_method_test("idiv", "idiv-method")

    def test_rdiv_method(self):
        self.defined_method_test("rdiv", "rdiv-method")

    def test_eq_and_hash_method(self):
        """Helper for verifying that a certain method is not defined."""
        node = astroid.extract_node(
            """
            class Foo(object):  #@
                def __eq__(self, other):
                    pass
                def __hash__(self):
                    pass"""
        )
        with self.assertNoMessages():
            self.checker.visit_classdef(node)

    def test_eq_and_hash_is_none(self):
        """Helper for verifying that a certain method is not defined."""
        node = astroid.extract_node(
            """
            class Foo(object):  #@
                def __eq__(self, other):
                    pass
                __hash__ = None"""
        )
        with self.assertNoMessages():
            self.checker.visit_classdef(node)

    def test_eq_without_hash_method(self):
        """Helper for verifying that a certain method is not defined."""
        node = astroid.extract_node(
            """
            class Foo(object):  #@
                def __eq__(self, other):
                    pass"""
        )
        message = testutils.Message("eq-without-hash", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_classdef(node)

    def test_relative_import(self):
        node = astroid.extract_node("import string  #@")
        message = testutils.Message("no-absolute-import", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_import(node)
        with self.assertNoMessages():
            # message should only be added once
            self.checker.visit_import(node)

    def test_relative_from_import(self):
        node = astroid.extract_node("from os import path  #@")
        message = testutils.Message("no-absolute-import", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_importfrom(node)
        with self.assertNoMessages():
            # message should only be added once
            self.checker.visit_importfrom(node)

    def test_absolute_import(self):
        module_import = astroid.parse(
            "from __future__ import absolute_import; import os"
        )
        module_from = astroid.parse(
            "from __future__ import absolute_import; from os import path"
        )
        with self.assertNoMessages():
            for module in (module_import, module_from):
                self.walk(module)

    def test_import_star_module_level(self):
        node = astroid.extract_node(
            """
        def test():
            from lala import * #@
        """
        )
        absolute = testutils.Message("no-absolute-import", node=node)
        star = testutils.Message("import-star-module-level", node=node)
        with self.assertAddsMessages(absolute, star):
            self.checker.visit_importfrom(node)

    def test_division(self):
        nodes = astroid.extract_node(
            """\
            from _unknown import a, b
            3 / 2  #@
            3 / int(a) #@
            int(a) / 3 #@
            a / b #@
            """
        )
        for node in nodes:
            message = testutils.Message("old-division", node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_binop(node)

    def test_division_with_future_statement(self):
        module = astroid.parse("from __future__ import division; 3 / 2")
        with self.assertNoMessages():
            self.walk(module)

    def test_floor_division(self):
        node = astroid.extract_node(" 3 // 2  #@")
        with self.assertNoMessages():
            self.checker.visit_binop(node)

    def test_division_by_float(self):
        nodes = astroid.extract_node(
            """\
            3.0 / 2  #@
            3 / 2.0  #@
            3 / float(a)  #@
            float(a) / 3  #@
            """
        )
        with self.assertNoMessages():
            for node in nodes:
                self.checker.visit_binop(node)

    def test_division_different_types(self):
        nodes = astroid.extract_node(
            """
        class A:
            pass
        A / 2 #@
        A() / 2 #@
        "a" / "a" #@
        class Path:
            def __div__(self, other):
                return 42
        Path() / 24 #@
        """
        )
        for node in nodes:
            with self.assertNoMessages():
                self.checker.visit_binop(node)

    def test_dict_iter_method(self):
        for meth in ("keys", "values", "items"):
            node = astroid.extract_node("x.iter%s()  #@" % meth)
            message = testutils.Message("dict-iter-method", node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_dict_iter_method_on_dict(self):
        nodes = astroid.extract_node(
            """
        from collections import defaultdict
        {}.iterkeys() #@
        defaultdict(list).iterkeys() #@
        class Someclass(dict):
            pass
        Someclass().iterkeys() #@

        # Emits even though we are not sure they are dicts
        x.iterkeys() #@

        def func(x):
            x.iterkeys() #@
        """
        )
        for node in nodes:
            message = testutils.Message("dict-iter-method", node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_dict_not_iter_method(self):
        arg_node = astroid.extract_node("x.iterkeys(x)  #@")
        stararg_node = astroid.extract_node("x.iterkeys(*x)  #@")
        kwarg_node = astroid.extract_node("x.iterkeys(y=x)  #@")
        with self.assertNoMessages():
            for node in (arg_node, stararg_node, kwarg_node):
                self.checker.visit_call(node)

    def test_dict_view_method(self):
        for meth in ("keys", "values", "items"):
            node = astroid.extract_node("x.view%s()  #@" % meth)
            message = testutils.Message("dict-view-method", node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_dict_viewkeys(self):
        nodes = astroid.extract_node(
            """
        from collections import defaultdict
        {}.viewkeys() #@
        defaultdict(list).viewkeys() #@
        class Someclass(dict):
            pass
        Someclass().viewkeys() #@

        # Emits even though they might not be dicts
        x.viewkeys() #@

        def func(x):
            x.viewkeys() #@
        """
        )
        for node in nodes:
            message = testutils.Message("dict-view-method", node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_next_method(self):
        node = astroid.extract_node("x.next()  #@")
        message = testutils.Message("next-method-called", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_not_next_method(self):
        arg_node = astroid.extract_node("x.next(x)  #@")
        stararg_node = astroid.extract_node("x.next(*x)  #@")
        kwarg_node = astroid.extract_node("x.next(y=x)  #@")
        with self.assertNoMessages():
            for node in (arg_node, stararg_node, kwarg_node):
                self.checker.visit_call(node)

    def test_metaclass_assignment(self):
        node = astroid.extract_node(
            """
            class Foo(object):  #@
                __metaclass__ = type"""
        )
        message = testutils.Message("metaclass-assignment", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_classdef(node)

    def test_metaclass_global_assignment(self):
        module = astroid.parse("__metaclass__ = type")
        with self.assertNoMessages():
            self.walk(module)

    def test_xreadlines_attribute(self):
        node = astroid.extract_node(
            """
        f.xreadlines #@
        """
        )
        message = testutils.Message("xreadlines-attribute", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_exception_message_attribute(self):
        node = astroid.extract_node(
            """
        try:
            raise Exception("test")
        except Exception as e:
            e.message #@
        """
        )
        message = testutils.Message("exception-message-attribute", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_normal_message_attribute(self):
        node = astroid.extract_node(
            """
        e.message #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    def test_invalid_codec(self):
        node = astroid.extract_node('foobar.encode("hex") #@')
        message = testutils.Message("invalid-str-codec", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_valid_codec(self):
        node = astroid.extract_node('foobar.encode("ascii", "ignore")  #@')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_visit_call_with_kwarg(self):
        node = astroid.extract_node('foobar.raz(encoding="hex")  #@')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_invalid_open_codec(self):
        node = astroid.extract_node('open(foobar, encoding="hex") #@')
        message = testutils.Message("invalid-str-codec", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_valid_open_codec(self):
        node = astroid.extract_node('open(foobar, encoding="palmos") #@')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_using_cmp_argument(self):
        nodes = astroid.extract_node(
            """
        [].sort(cmp=lambda x: x) #@
        a = list(range(x))
        a.sort(cmp=lambda x: x) #@

        sorted([], cmp=lambda x: x) #@
        """
        )
        for node in nodes:
            message = testutils.Message("using-cmp-argument", node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_sys_maxint(self):
        node = astroid.extract_node(
            """
        import sys
        sys.maxint #@
        """
        )
        message = testutils.Message("sys-max-int", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_itertools_izip(self):
        node = astroid.extract_node(
            """
        from itertools import izip #@
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        message = testutils.Message("deprecated-itertools-function", node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_importfrom(node)

    def test_deprecated_types_fields(self):
        node = astroid.extract_node(
            """
        from types import StringType #@
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        message = testutils.Message("deprecated-types-field", node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_importfrom(node)

    def test_sys_maxint_imort_from(self):
        node = astroid.extract_node(
            """
        from sys import maxint #@
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        message = testutils.Message("sys-max-int", node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_importfrom(node)

    def test_object_maxint(self):
        node = astroid.extract_node(
            """
        sys = object()
        sys.maxint #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    def test_bad_import(self):
        node = astroid.extract_node(
            """
        import urllib2, sys #@
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        message = testutils.Message("bad-python3-import", node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_import(node)

    def test_bad_import_turtle(self):
        node = astroid.extract_node(
            """
        import turtle #@
        turtle.Turtle()
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_import(node)

    def test_bad_import_dbm(self):
        node = astroid.extract_node(
            """
        from dbm import open as open_ #@
        open_("dummy.db")
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_importfrom(node)

    def test_bad_import_conditional(self):
        node = astroid.extract_node(
            """
        import six
        if six.PY2:
            import urllib2 #@
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_import(node)

    def test_bad_import_try_except_handler(self):
        node = astroid.extract_node(
            """
        try:
            from hashlib import sha
        except:
            import sha #@
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_import(node)

    def test_bad_import_try(self):
        node = astroid.extract_node(
            """
        try:
            import md5  #@
        except:
            from hashlib import md5
        finally:
            pass
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_import(node)

    def test_bad_import_try_finally(self):
        node = astroid.extract_node(
            """
        try:
            import Queue  #@
        finally:
            import queue
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        message = testutils.Message("bad-python3-import", node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_import(node)

    def test_bad_import_from(self):
        node = astroid.extract_node(
            """
        from cStringIO import StringIO #@
        """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        message = testutils.Message("bad-python3-import", node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_importfrom(node)

    def test_bad_string_attribute(self):
        node = astroid.extract_node(
            """
        import string
        string.maketrans #@
        """
        )
        message = testutils.Message("deprecated-string-function", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_bad_operator_attribute(self):
        node = astroid.extract_node(
            """
        import operator
        operator.div #@
        """
        )
        message = testutils.Message("deprecated-operator-function", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_comprehension_escape(self):
        assign, escaped_node = astroid.extract_node(
            """
        a = [i for i in range(10)] #@
        i #@
        """
        )
        good_module = astroid.parse(
            """
        {c for c in range(10)} #@
        {j:j for j in range(10)} #@
        [image_child] = [x for x in range(10)]
        thumbnail = func(__(image_child))
        """
        )
        message = testutils.Message("comprehension-escape", node=escaped_node)
        with self.assertAddsMessages(message):
            self.checker.visit_listcomp(assign.value)

        with self.assertNoMessages():
            self.walk(good_module)

    def test_comprehension_escape_newly_introduced(self):
        node = astroid.extract_node(
            """
        [i for i in range(3)]
        for i in range(3):
            i
        """
        )
        with self.assertNoMessages():
            self.walk(node)

    def test_exception_escape(self):
        module = astroid.parse(
            """
        try: 1/0
        except ValueError as exc:
            pass
        exc #@
        try:
           2/0
        except (ValueError, TypeError) as exc:
           exc = 2
        exc #@
        try:
           2/0
        except (ValueError, TypeError): #@
           exc = 2
        exc #@
        try:
           1/0
        except (ValueError, TypeError) as exc:
           foo(bar for bar in exc.bar)
        """
        )
        message = testutils.Message("exception-escape", node=module.body[1].value)
        with self.assertAddsMessages(message):
            self.checker.visit_excepthandler(module.body[0].handlers[0])
        with self.assertNoMessages():
            self.checker.visit_excepthandler(module.body[2].handlers[0])
            self.checker.visit_excepthandler(module.body[4].handlers[0])
            self.checker.visit_excepthandler(module.body[6].handlers[0])

    def test_bad_sys_attribute(self):
        node = astroid.extract_node(
            """
        import sys
        sys.exc_clear #@
        """
        )
        message = testutils.Message("deprecated-sys-function", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_bad_urllib_attribute(self):
        nodes = astroid.extract_node(
            """
        import urllib
        urllib.addbase #@
        urllib.splithost #@
        urllib.urlretrieve #@
        urllib.urlopen #@
        urllib.urlencode #@
        """
        )
        for node in nodes:
            message = testutils.Message("deprecated-urllib-function", node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_attribute(node)

    def test_ok_string_attribute(self):
        node = astroid.extract_node(
            """
        import string
        string.ascii_letters #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    def test_bad_string_call(self):
        node = astroid.extract_node(
            """
        import string
        string.upper("hello world") #@
        """
        )
        message = testutils.Message("deprecated-string-function", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_ok_shadowed_call(self):
        node = astroid.extract_node(
            """
        import six.moves.configparser
        six.moves.configparser.ConfigParser() #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_ok_string_call(self):
        node = astroid.extract_node(
            """
        import string
        string.Foramtter() #@
        """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_bad_string_import_from(self):
        node = astroid.extract_node(
            """
         from string import atoi #@
         """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        message = testutils.Message("deprecated-string-function", node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_importfrom(node)

    def test_ok_string_import_from(self):
        node = astroid.extract_node(
            """
         from string import digits #@
         """
        )
        absolute_import_message = testutils.Message("no-absolute-import", node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_importfrom(node)

    def test_bad_str_translate_call_string_literal(self):
        node = astroid.extract_node(
            """
         foobar.translate(None, 'abc123') #@
         """
        )
        message = testutils.Message(
            "deprecated-str-translate-call", node=node, confidence=INFERENCE_FAILURE
        )
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_bad_str_translate_call_variable(self):
        node = astroid.extract_node(
            """
         def raz(foobar):
           foobar.translate(None, 'hello') #@
         """
        )
        message = testutils.Message(
            "deprecated-str-translate-call", node=node, confidence=INFERENCE_FAILURE
        )
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_bad_str_translate_call_infer_str(self):
        node = astroid.extract_node(
            """
         foobar = "hello world"
         foobar.translate(None, foobar) #@
         """
        )
        message = testutils.Message(
            "deprecated-str-translate-call", node=node, confidence=INFERENCE
        )
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_ok_str_translate_call_integer(self):
        node = astroid.extract_node(
            """
         foobar.translate(None, 33) #@
         """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_ok_str_translate_call_keyword(self):
        node = astroid.extract_node(
            """
         foobar.translate(None, 'foobar', raz=33) #@
         """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_ok_str_translate_call_not_str(self):
        node = astroid.extract_node(
            """
         foobar = {}
         foobar.translate(None, 'foobar') #@
         """
        )
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_non_py2_conditional(self):
        code = """
        from __future__ import absolute_import
        import sys
        x = {}
        if sys.maxsize:
            x.iterkeys()  #@
        """
        node = astroid.extract_node(code)
        module = node.parent.parent
        message = testutils.Message("dict-iter-method", node=node)
        with self.assertAddsMessages(message):
            self.walk(module)

    def test_six_conditional(self):
        code = """
        from __future__ import absolute_import
        import six
        x = {}
        if six.PY2:
            x.iterkeys()
        """
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def test_versioninfo_conditional(self):
        code = """
        from __future__ import absolute_import
        import sys
        x = {}
        if sys.version_info[0] == 2:
            x.iterkeys()
        """
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def test_versioninfo_tuple_conditional(self):
        code = """
        from __future__ import absolute_import
        import sys
        x = {}
        if sys.version_info == (2, 7):
            x.iterkeys()
        """
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def test_six_ifexp_conditional(self):
        code = """
        from __future__ import absolute_import
        import six
        import string
        string.translate if six.PY2 else None
        """
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def test_next_defined(self):
        node = astroid.extract_node(
            """
            class Foo(object):
                def next(self):  #@
                    pass"""
        )
        message = testutils.Message("next-method-defined", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(node)

    def test_next_defined_too_many_args(self):
        node = astroid.extract_node(
            """
            class Foo(object):
                def next(self, foo=None):  #@
                    pass"""
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_next_defined_static_method_too_many_args(self):
        node = astroid.extract_node(
            """
            class Foo(object):
                @staticmethod
                def next(self):  #@
                    pass"""
        )
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_next_defined_static_method(self):
        node = astroid.extract_node(
            """
            class Foo(object):
                @staticmethod
                def next():  #@
                    pass"""
        )
        message = testutils.Message("next-method-defined", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(node)

    def test_next_defined_class_method(self):
        node = astroid.extract_node(
            """
            class Foo(object):
                @classmethod
                def next(cls):  #@
                    pass"""
        )
        message = testutils.Message("next-method-defined", node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(node)
