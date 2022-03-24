# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Basic checker for Python code."""

__all__ = [
    "NameChecker",
    "NamingStyle",
    "KNOWN_NAME_TYPES_WITH_STYLE",
    "SnakeCaseStyle",
    "CamelCaseStyle",
    "UpperCaseStyle",
    "PascalCaseStyle",
    "AnyStyle",
]

import collections
import itertools
import sys
from typing import TYPE_CHECKING, Any, Dict, Iterator, Optional, cast

import astroid
from astroid import nodes

from pylint import interfaces
from pylint import utils as lint_utils
from pylint.checkers import utils
from pylint.checkers.base.basic_checker import _BasicChecker
from pylint.checkers.base.comparison_checker import ComparisonChecker
from pylint.checkers.base.docstring_checker import DocStringChecker
from pylint.checkers.base.name_checker import (
    KNOWN_NAME_TYPES_WITH_STYLE,
    AnyStyle,
    CamelCaseStyle,
    NamingStyle,
    PascalCaseStyle,
    SnakeCaseStyle,
    UpperCaseStyle,
)
from pylint.checkers.base.name_checker.checker import NameChecker
from pylint.checkers.base.pass_checker import PassChecker
from pylint.checkers.utils import infer_all
from pylint.reporters.ureports import nodes as reporter_nodes
from pylint.utils import LinterStats
from pylint.utils.utils import get_global_option

if TYPE_CHECKING:
    from pylint.lint import PyLinter

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


REVERSED_PROTOCOL_METHOD = "__reversed__"
SEQUENCE_PROTOCOL_METHODS = ("__getitem__", "__len__")
REVERSED_METHODS = (SEQUENCE_PROTOCOL_METHODS, (REVERSED_PROTOCOL_METHOD,))
UNITTEST_CASE = "unittest.case"
ABC_METACLASSES = {"_py_abc.ABCMeta", "abc.ABCMeta"}  # Python 3.7+,


# A mapping from qname -> symbol, to be used when generating messages
# about dangerous default values as arguments
DEFAULT_ARGUMENT_SYMBOLS = dict(
    zip(
        [".".join(["builtins", x]) for x in ("set", "dict", "list")],
        ["set()", "{}", "[]"],
    ),
    **{
        x: f"{x}()"
        for x in (
            "collections.deque",
            "collections.ChainMap",
            "collections.Counter",
            "collections.OrderedDict",
            "collections.defaultdict",
            "collections.UserDict",
            "collections.UserList",
        )
    },
)


# List of methods which can be redefined
REDEFINABLE_METHODS = frozenset(("__module__",))
TYPING_FORWARD_REF_QNAME = "typing.ForwardRef"


LOOPLIKE_NODES = (
    nodes.For,
    nodes.ListComp,
    nodes.SetComp,
    nodes.DictComp,
    nodes.GeneratorExp,
)


def in_loop(node: nodes.NodeNG) -> bool:
    """Return whether the node is inside a kind of for loop."""
    return any(isinstance(parent, LOOPLIKE_NODES) for parent in node.node_ancestors())


def in_nested_list(nested_list, obj):
    """Return true if the object is an element of <nested_list> or of a nested
    list
    """
    for elmt in nested_list:
        if isinstance(elmt, (list, tuple)):
            if in_nested_list(elmt, obj):
                return True
        elif elmt == obj:
            return True
    return False


def _get_break_loop_node(break_node):
    """Returns the loop node that holds the break node in arguments.

    Args:
        break_node (astroid.Break): the break node of interest.

    Returns:
        astroid.For or astroid.While: the loop node holding the break node.
    """
    loop_nodes = (nodes.For, nodes.While)
    parent = break_node.parent
    while not isinstance(parent, loop_nodes) or break_node in getattr(
        parent, "orelse", []
    ):
        break_node = parent
        parent = parent.parent
        if parent is None:
            break
    return parent


def _loop_exits_early(loop):
    """Returns true if a loop may end with a break statement.

    Args:
        loop (astroid.For, astroid.While): the loop node inspected.

    Returns:
        bool: True if the loop may end with a break statement, False otherwise.
    """
    loop_nodes = (nodes.For, nodes.While)
    definition_nodes = (nodes.FunctionDef, nodes.ClassDef)
    inner_loop_nodes = [
        _node
        for _node in loop.nodes_of_class(loop_nodes, skip_klass=definition_nodes)
        if _node != loop
    ]
    return any(
        _node
        for _node in loop.nodes_of_class(nodes.Break, skip_klass=definition_nodes)
        if _get_break_loop_node(_node) not in inner_loop_nodes
    )


def _has_abstract_methods(node):
    """Determine if the given `node` has abstract methods.

    The methods should be made abstract by decorating them
    with `abc` decorators.
    """
    return len(utils.unimplemented_abstract_methods(node)) > 0


def report_by_type_stats(
    sect,
    stats: LinterStats,
    old_stats: Optional[LinterStats],
):
    """Make a report of.

    * percentage of different types documented
    * percentage of different types with a bad name
    """
    # percentage of different types documented and/or with a bad name
    nice_stats: Dict[str, Dict[str, str]] = {}
    for node_type in ("module", "class", "method", "function"):
        node_type = cast(Literal["function", "class", "method", "module"], node_type)
        total = stats.get_node_count(node_type)
        nice_stats[node_type] = {}
        if total != 0:
            undocumented_node = stats.get_undocumented(node_type)
            documented = total - undocumented_node
            percent = (documented * 100.0) / total
            nice_stats[node_type]["percent_documented"] = f"{percent:.2f}"
            badname_node = stats.get_bad_names(node_type)
            percent = (badname_node * 100.0) / total
            nice_stats[node_type]["percent_badname"] = f"{percent:.2f}"
    lines = ["type", "number", "old number", "difference", "%documented", "%badname"]
    for node_type in ("module", "class", "method", "function"):
        node_type = cast(Literal["function", "class", "method", "module"], node_type)
        new = stats.get_node_count(node_type)
        old = old_stats.get_node_count(node_type) if old_stats else None
        diff_str = lint_utils.diff_string(old, new) if old else None
        lines += [
            node_type,
            str(new),
            str(old) if old else "NC",
            diff_str if diff_str else "NC",
            nice_stats[node_type].get("percent_documented", "0"),
            nice_stats[node_type].get("percent_badname", "0"),
        ]
    sect.append(reporter_nodes.Table(children=lines, cols=6, rheaders=1))


def redefined_by_decorator(node):
    """Return True if the object is a method redefined via decorator.

    For example:
        @property
        def x(self): return self._x
        @x.setter
        def x(self, value): self._x = value
    """
    if node.decorators:
        for decorator in node.decorators.nodes:
            if (
                isinstance(decorator, nodes.Attribute)
                and getattr(decorator.expr, "name", None) == node.name
            ):
                return True
    return False


class BasicErrorChecker(_BasicChecker):
    msgs = {
        "E0100": (
            "__init__ method is a generator",
            "init-is-generator",
            "Used when the special class method __init__ is turned into a "
            "generator by a yield in its body.",
        ),
        "E0101": (
            "Explicit return in __init__",
            "return-in-init",
            "Used when the special class method __init__ has an explicit "
            "return value.",
        ),
        "E0102": (
            "%s already defined line %s",
            "function-redefined",
            "Used when a function / class / method is redefined.",
        ),
        "E0103": (
            "%r not properly in loop",
            "not-in-loop",
            "Used when break or continue keywords are used outside a loop.",
        ),
        "E0104": (
            "Return outside function",
            "return-outside-function",
            'Used when a "return" statement is found outside a function or method.',
        ),
        "E0105": (
            "Yield outside function",
            "yield-outside-function",
            'Used when a "yield" statement is found outside a function or method.',
        ),
        "E0106": (
            "Return with argument inside generator",
            "return-arg-in-generator",
            'Used when a "return" statement with an argument is found '
            "outside in a generator function or method (e.g. with some "
            '"yield" statements).',
            {"maxversion": (3, 3)},
        ),
        "E0107": (
            "Use of the non-existent %s operator",
            "nonexistent-operator",
            "Used when you attempt to use the C-style pre-increment or "
            "pre-decrement operator -- and ++, which doesn't exist in Python.",
        ),
        "E0108": (
            "Duplicate argument name %s in function definition",
            "duplicate-argument-name",
            "Duplicate argument names in function definitions are syntax errors.",
        ),
        "E0110": (
            "Abstract class %r with abstract methods instantiated",
            "abstract-class-instantiated",
            "Used when an abstract class with `abc.ABCMeta` as metaclass "
            "has abstract methods and is instantiated.",
        ),
        "W0120": (
            "Else clause on loop without a break statement, remove the else and"
            " de-indent all the code inside it",
            "useless-else-on-loop",
            "Loops should only have an else clause if they can exit early "
            "with a break statement, otherwise the statements under else "
            "should be on the same scope as the loop itself.",
        ),
        "E0112": (
            "More than one starred expression in assignment",
            "too-many-star-expressions",
            "Emitted when there are more than one starred "
            "expressions (`*x`) in an assignment. This is a SyntaxError.",
        ),
        "E0113": (
            "Starred assignment target must be in a list or tuple",
            "invalid-star-assignment-target",
            "Emitted when a star expression is used as a starred assignment target.",
        ),
        "E0114": (
            "Can use starred expression only in assignment target",
            "star-needs-assignment-target",
            "Emitted when a star expression is not used in an assignment target.",
        ),
        "E0115": (
            "Name %r is nonlocal and global",
            "nonlocal-and-global",
            "Emitted when a name is both nonlocal and global.",
        ),
        "E0116": (
            "'continue' not supported inside 'finally' clause",
            "continue-in-finally",
            "Emitted when the `continue` keyword is found "
            "inside a finally clause, which is a SyntaxError.",
            {"maxversion": (3, 8)},
        ),
        "E0117": (
            "nonlocal name %s found without binding",
            "nonlocal-without-binding",
            "Emitted when a nonlocal variable does not have an attached "
            "name somewhere in the parent scopes",
        ),
        "E0118": (
            "Name %r is used prior to global declaration",
            "used-prior-global-declaration",
            "Emitted when a name is used prior a global declaration, "
            "which results in an error since Python 3.6.",
            {"minversion": (3, 6)},
        ),
    }

    @utils.check_messages("function-redefined")
    def visit_classdef(self, node: nodes.ClassDef) -> None:
        self._check_redefinition("class", node)

    def _too_many_starred_for_tuple(self, assign_tuple):
        starred_count = 0
        for elem in assign_tuple.itered():
            if isinstance(elem, nodes.Tuple):
                return self._too_many_starred_for_tuple(elem)
            if isinstance(elem, nodes.Starred):
                starred_count += 1
        return starred_count > 1

    @utils.check_messages("too-many-star-expressions", "invalid-star-assignment-target")
    def visit_assign(self, node: nodes.Assign) -> None:
        # Check *a, *b = ...
        assign_target = node.targets[0]
        # Check *a = b
        if isinstance(node.targets[0], nodes.Starred):
            self.add_message("invalid-star-assignment-target", node=node)

        if not isinstance(assign_target, nodes.Tuple):
            return
        if self._too_many_starred_for_tuple(assign_target):
            self.add_message("too-many-star-expressions", node=node)

    @utils.check_messages("star-needs-assignment-target")
    def visit_starred(self, node: nodes.Starred) -> None:
        """Check that a Starred expression is used in an assignment target."""
        if isinstance(node.parent, nodes.Call):
            # f(*args) is converted to Call(args=[Starred]), so ignore
            # them for this check.
            return
        if isinstance(node.parent, (nodes.List, nodes.Tuple, nodes.Set, nodes.Dict)):
            # PEP 448 unpacking.
            return

        stmt = node.statement(future=True)
        if not isinstance(stmt, nodes.Assign):
            return

        if stmt.value is node or stmt.value.parent_of(node):
            self.add_message("star-needs-assignment-target", node=node)

    @utils.check_messages(
        "init-is-generator",
        "return-in-init",
        "function-redefined",
        "return-arg-in-generator",
        "duplicate-argument-name",
        "nonlocal-and-global",
        "used-prior-global-declaration",
    )
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        self._check_nonlocal_and_global(node)
        self._check_name_used_prior_global(node)
        if not redefined_by_decorator(
            node
        ) and not utils.is_registered_in_singledispatch_function(node):
            self._check_redefinition(node.is_method() and "method" or "function", node)
        # checks for max returns, branch, return in __init__
        returns = node.nodes_of_class(
            nodes.Return, skip_klass=(nodes.FunctionDef, nodes.ClassDef)
        )
        if node.is_method() and node.name == "__init__":
            if node.is_generator():
                self.add_message("init-is-generator", node=node)
            else:
                values = [r.value for r in returns]
                # Are we returning anything but None from constructors
                if any(v for v in values if not utils.is_none(v)):
                    self.add_message("return-in-init", node=node)
        # Check for duplicate names by clustering args with same name for detailed report
        arg_clusters = collections.defaultdict(list)
        arguments: Iterator[Any] = filter(None, [node.args.args, node.args.kwonlyargs])

        for arg in itertools.chain.from_iterable(arguments):
            arg_clusters[arg.name].append(arg)

        # provide detailed report about each repeated argument
        for argument_duplicates in arg_clusters.values():
            if len(argument_duplicates) != 1:
                for argument in argument_duplicates:
                    self.add_message(
                        "duplicate-argument-name",
                        line=argument.lineno,
                        node=argument,
                        args=(argument.name,),
                    )

    visit_asyncfunctiondef = visit_functiondef

    def _check_name_used_prior_global(self, node):

        scope_globals = {
            name: child
            for child in node.nodes_of_class(nodes.Global)
            for name in child.names
            if child.scope() is node
        }

        if not scope_globals:
            return

        for node_name in node.nodes_of_class(nodes.Name):
            if node_name.scope() is not node:
                continue

            name = node_name.name
            corresponding_global = scope_globals.get(name)
            if not corresponding_global:
                continue

            global_lineno = corresponding_global.fromlineno
            if global_lineno and global_lineno > node_name.fromlineno:
                self.add_message(
                    "used-prior-global-declaration", node=node_name, args=(name,)
                )

    def _check_nonlocal_and_global(self, node):
        """Check that a name is both nonlocal and global."""

        def same_scope(current):
            return current.scope() is node

        from_iter = itertools.chain.from_iterable
        nonlocals = set(
            from_iter(
                child.names
                for child in node.nodes_of_class(nodes.Nonlocal)
                if same_scope(child)
            )
        )

        if not nonlocals:
            return

        global_vars = set(
            from_iter(
                child.names
                for child in node.nodes_of_class(nodes.Global)
                if same_scope(child)
            )
        )
        for name in nonlocals.intersection(global_vars):
            self.add_message("nonlocal-and-global", args=(name,), node=node)

    @utils.check_messages("return-outside-function")
    def visit_return(self, node: nodes.Return) -> None:
        if not isinstance(node.frame(future=True), nodes.FunctionDef):
            self.add_message("return-outside-function", node=node)

    @utils.check_messages("yield-outside-function")
    def visit_yield(self, node: nodes.Yield) -> None:
        self._check_yield_outside_func(node)

    @utils.check_messages("yield-outside-function")
    def visit_yieldfrom(self, node: nodes.YieldFrom) -> None:
        self._check_yield_outside_func(node)

    @utils.check_messages("not-in-loop", "continue-in-finally")
    def visit_continue(self, node: nodes.Continue) -> None:
        self._check_in_loop(node, "continue")

    @utils.check_messages("not-in-loop")
    def visit_break(self, node: nodes.Break) -> None:
        self._check_in_loop(node, "break")

    @utils.check_messages("useless-else-on-loop")
    def visit_for(self, node: nodes.For) -> None:
        self._check_else_on_loop(node)

    @utils.check_messages("useless-else-on-loop")
    def visit_while(self, node: nodes.While) -> None:
        self._check_else_on_loop(node)

    @utils.check_messages("nonexistent-operator")
    def visit_unaryop(self, node: nodes.UnaryOp) -> None:
        """Check use of the non-existent ++ and -- operators."""
        if (
            (node.op in "+-")
            and isinstance(node.operand, nodes.UnaryOp)
            and (node.operand.op == node.op)
        ):
            self.add_message("nonexistent-operator", node=node, args=node.op * 2)

    def _check_nonlocal_without_binding(self, node, name):
        current_scope = node.scope()
        while True:
            if current_scope.parent is None:
                break

            if not isinstance(current_scope, (nodes.ClassDef, nodes.FunctionDef)):
                self.add_message("nonlocal-without-binding", args=(name,), node=node)
                return

            if name not in current_scope.locals:
                current_scope = current_scope.parent.scope()
                continue

            # Okay, found it.
            return

        if not isinstance(current_scope, nodes.FunctionDef):
            self.add_message("nonlocal-without-binding", args=(name,), node=node)

    @utils.check_messages("nonlocal-without-binding")
    def visit_nonlocal(self, node: nodes.Nonlocal) -> None:
        for name in node.names:
            self._check_nonlocal_without_binding(node, name)

    @utils.check_messages("abstract-class-instantiated")
    def visit_call(self, node: nodes.Call) -> None:
        """Check instantiating abstract class with
        abc.ABCMeta as metaclass.
        """
        for inferred in infer_all(node.func):
            self._check_inferred_class_is_abstract(inferred, node)

    def _check_inferred_class_is_abstract(self, inferred, node):
        if not isinstance(inferred, nodes.ClassDef):
            return

        klass = utils.node_frame_class(node)
        if klass is inferred:
            # Don't emit the warning if the class is instantiated
            # in its own body or if the call is not an instance
            # creation. If the class is instantiated into its own
            # body, we're expecting that it knows what it is doing.
            return

        # __init__ was called
        abstract_methods = _has_abstract_methods(inferred)

        if not abstract_methods:
            return

        metaclass = inferred.metaclass()

        if metaclass is None:
            # Python 3.4 has `abc.ABC`, which won't be detected
            # by ClassNode.metaclass()
            for ancestor in inferred.ancestors():
                if ancestor.qname() == "abc.ABC":
                    self.add_message(
                        "abstract-class-instantiated", args=(inferred.name,), node=node
                    )
                    break

            return

        if metaclass.qname() in ABC_METACLASSES:
            self.add_message(
                "abstract-class-instantiated", args=(inferred.name,), node=node
            )

    def _check_yield_outside_func(self, node):
        if not isinstance(node.frame(future=True), (nodes.FunctionDef, nodes.Lambda)):
            self.add_message("yield-outside-function", node=node)

    def _check_else_on_loop(self, node):
        """Check that any loop with an else clause has a break statement."""
        if node.orelse and not _loop_exits_early(node):
            self.add_message(
                "useless-else-on-loop",
                node=node,
                # This is not optimal, but the line previous
                # to the first statement in the else clause
                # will usually be the one that contains the else:.
                line=node.orelse[0].lineno - 1,
            )

    def _check_in_loop(self, node, node_name):
        """Check that a node is inside a for or while loop."""
        for parent in node.node_ancestors():
            if isinstance(parent, (nodes.For, nodes.While)):
                if node not in parent.orelse:
                    return

            if isinstance(parent, (nodes.ClassDef, nodes.FunctionDef)):
                break
            if (
                isinstance(parent, nodes.TryFinally)
                and node in parent.finalbody
                and isinstance(node, nodes.Continue)
            ):
                self.add_message("continue-in-finally", node=node)

        self.add_message("not-in-loop", node=node, args=node_name)

    def _check_redefinition(self, redeftype, node):
        """Check for redefinition of a function / method / class name."""
        parent_frame = node.parent.frame(future=True)

        # Ignore function stubs created for type information
        redefinitions = [
            i
            for i in parent_frame.locals[node.name]
            if not (isinstance(i.parent, nodes.AnnAssign) and i.parent.simple)
        ]
        defined_self = next(
            (local for local in redefinitions if not utils.is_overload_stub(local)),
            node,
        )
        if defined_self is not node and not astroid.are_exclusive(node, defined_self):
            # Additional checks for methods which are not considered
            # redefined, since they are already part of the base API.
            if (
                isinstance(parent_frame, nodes.ClassDef)
                and node.name in REDEFINABLE_METHODS
            ):
                return

            # Skip typing.overload() functions.
            if utils.is_overload_stub(node):
                return

            # Exempt functions redefined on a condition.
            if isinstance(node.parent, nodes.If):
                # Exempt "if not <func>" cases
                if (
                    isinstance(node.parent.test, nodes.UnaryOp)
                    and node.parent.test.op == "not"
                    and isinstance(node.parent.test.operand, nodes.Name)
                    and node.parent.test.operand.name == node.name
                ):
                    return

                # Exempt "if <func> is not None" cases
                # pylint: disable=too-many-boolean-expressions
                if (
                    isinstance(node.parent.test, nodes.Compare)
                    and isinstance(node.parent.test.left, nodes.Name)
                    and node.parent.test.left.name == node.name
                    and node.parent.test.ops[0][0] == "is"
                    and isinstance(node.parent.test.ops[0][1], nodes.Const)
                    and node.parent.test.ops[0][1].value is None
                ):
                    return

            # Check if we have forward references for this node.
            try:
                redefinition_index = redefinitions.index(node)
            except ValueError:
                pass
            else:
                for redefinition in redefinitions[:redefinition_index]:
                    inferred = utils.safe_infer(redefinition)
                    if (
                        inferred
                        and isinstance(inferred, astroid.Instance)
                        and inferred.qname() == TYPING_FORWARD_REF_QNAME
                    ):
                        return

            dummy_variables_rgx = lint_utils.get_global_option(
                self, "dummy-variables-rgx", default=None
            )
            if dummy_variables_rgx and dummy_variables_rgx.match(node.name):
                return
            self.add_message(
                "function-redefined",
                node=node,
                args=(redeftype, defined_self.fromlineno),
            )


class BasicChecker(_BasicChecker):
    """Basic checker.

    Checks for :
    * doc strings
    * number of arguments, local variables, branches, returns and statements in
    functions, methods
    * required module attributes
    * dangerous default values as arguments
    * redefinition of function / method / class
    * uses of the global statement
    """

    __implements__ = interfaces.IAstroidChecker

    name = "basic"
    msgs = {
        "W0101": (
            "Unreachable code",
            "unreachable",
            'Used when there is some code behind a "return" or "raise" '
            "statement, which will never be accessed.",
        ),
        "W0102": (
            "Dangerous default value %s as argument",
            "dangerous-default-value",
            "Used when a mutable value as list or dictionary is detected in "
            "a default value for an argument.",
        ),
        "W0104": (
            "Statement seems to have no effect",
            "pointless-statement",
            "Used when a statement doesn't have (or at least seems to) any effect.",
        ),
        "W0105": (
            "String statement has no effect",
            "pointless-string-statement",
            "Used when a string is used as a statement (which of course "
            "has no effect). This is a particular case of W0104 with its "
            "own message so you can easily disable it if you're using "
            "those strings as documentation, instead of comments.",
        ),
        "W0106": (
            'Expression "%s" is assigned to nothing',
            "expression-not-assigned",
            "Used when an expression that is not a function call is assigned "
            "to nothing. Probably something else was intended.",
        ),
        "W0108": (
            "Lambda may not be necessary",
            "unnecessary-lambda",
            "Used when the body of a lambda expression is a function call "
            "on the same argument list as the lambda itself; such lambda "
            "expressions are in all but a few cases replaceable with the "
            "function being called in the body of the lambda.",
        ),
        "W0109": (
            "Duplicate key %r in dictionary",
            "duplicate-key",
            "Used when a dictionary expression binds the same key multiple times.",
        ),
        "W0122": (
            "Use of exec",
            "exec-used",
            'Used when you use the "exec" statement (function for Python '
            "3), to discourage its usage. That doesn't "
            "mean you cannot use it !",
        ),
        "W0123": (
            "Use of eval",
            "eval-used",
            'Used when you use the "eval" function, to discourage its '
            "usage. Consider using `ast.literal_eval` for safely evaluating "
            "strings containing Python expressions "
            "from untrusted sources.",
        ),
        "W0150": (
            "%s statement in finally block may swallow exception",
            "lost-exception",
            "Used when a break or a return statement is found inside the "
            "finally clause of a try...finally block: the exceptions raised "
            "in the try clause will be silently swallowed instead of being "
            "re-raised.",
        ),
        "W0199": (
            "Assert called on a 2-item-tuple. Did you mean 'assert x,y'?",
            "assert-on-tuple",
            "A call of assert on a tuple will always evaluate to true if "
            "the tuple is not empty, and will always evaluate to false if "
            "it is.",
        ),
        "W0124": (
            'Following "as" with another context manager looks like a tuple.',
            "confusing-with-statement",
            "Emitted when a `with` statement component returns multiple values "
            "and uses name binding with `as` only for a part of those values, "
            "as in with ctx() as a, b. This can be misleading, since it's not "
            "clear if the context manager returns a tuple or if the node without "
            "a name binding is another context manager.",
        ),
        "W0125": (
            "Using a conditional statement with a constant value",
            "using-constant-test",
            "Emitted when a conditional statement (If or ternary if) "
            "uses a constant value for its test. This might not be what "
            "the user intended to do.",
        ),
        "W0126": (
            "Using a conditional statement with potentially wrong function or method call due to missing parentheses",
            "missing-parentheses-for-call-in-test",
            "Emitted when a conditional statement (If or ternary if) "
            "seems to wrongly call a function due to missing parentheses",
        ),
        "W0127": (
            "Assigning the same variable %r to itself",
            "self-assigning-variable",
            "Emitted when we detect that a variable is assigned to itself",
        ),
        "W0128": (
            "Redeclared variable %r in assignment",
            "redeclared-assigned-name",
            "Emitted when we detect that a variable was redeclared in the same assignment.",
        ),
        "E0111": (
            "The first reversed() argument is not a sequence",
            "bad-reversed-sequence",
            "Used when the first argument to reversed() builtin "
            "isn't a sequence (does not implement __reversed__, "
            "nor __getitem__ and __len__",
        ),
        "E0119": (
            "format function is not called on str",
            "misplaced-format-function",
            "Emitted when format function is not called on str object. "
            'e.g doing print("value: {}").format(123) instead of '
            'print("value: {}".format(123)). This might not be what the user '
            "intended to do.",
        ),
        "W0129": (
            "Assert statement has a string literal as its first argument. The assert will %s fail.",
            "assert-on-string-literal",
            "Used when an assert statement has a string literal as its first argument, which will "
            "cause the assert to always pass.",
        ),
    }

    reports = (("RP0101", "Statistics by type", report_by_type_stats),)

    def __init__(self, linter):
        super().__init__(linter)
        self._tryfinallys = None

    def open(self):
        """Initialize visit variables and statistics."""
        py_version = get_global_option(self, "py-version")
        self._py38_plus = py_version >= (3, 8)
        self._tryfinallys = []
        self.linter.stats.reset_node_count()

    @utils.check_messages("using-constant-test", "missing-parentheses-for-call-in-test")
    def visit_if(self, node: nodes.If) -> None:
        self._check_using_constant_test(node, node.test)

    @utils.check_messages("using-constant-test", "missing-parentheses-for-call-in-test")
    def visit_ifexp(self, node: nodes.IfExp) -> None:
        self._check_using_constant_test(node, node.test)

    @utils.check_messages("using-constant-test", "missing-parentheses-for-call-in-test")
    def visit_comprehension(self, node: nodes.Comprehension) -> None:
        if node.ifs:
            for if_test in node.ifs:
                self._check_using_constant_test(node, if_test)

    def _check_using_constant_test(self, node, test):
        const_nodes = (
            nodes.Module,
            nodes.GeneratorExp,
            nodes.Lambda,
            nodes.FunctionDef,
            nodes.ClassDef,
            astroid.bases.Generator,
            astroid.UnboundMethod,
            astroid.BoundMethod,
            nodes.Module,
        )
        structs = (nodes.Dict, nodes.Tuple, nodes.Set, nodes.List)

        # These nodes are excepted, since they are not constant
        # values, requiring a computation to happen.
        except_nodes = (
            nodes.Call,
            nodes.BinOp,
            nodes.BoolOp,
            nodes.UnaryOp,
            nodes.Subscript,
        )
        inferred = None
        emit = isinstance(test, (nodes.Const,) + structs + const_nodes)
        if not isinstance(test, except_nodes):
            inferred = utils.safe_infer(test)

        if emit:
            self.add_message("using-constant-test", node=node)
        elif isinstance(inferred, const_nodes):
            # If the constant node is a FunctionDef or Lambda then
            # it may be an illicit function call due to missing parentheses
            call_inferred = None
            try:
                if isinstance(inferred, nodes.FunctionDef):
                    call_inferred = inferred.infer_call_result()
                elif isinstance(inferred, nodes.Lambda):
                    call_inferred = inferred.infer_call_result(node)
            except astroid.InferenceError:
                call_inferred = None
            if call_inferred:
                try:
                    for inf_call in call_inferred:
                        if inf_call != astroid.Uninferable:
                            self.add_message(
                                "missing-parentheses-for-call-in-test", node=node
                            )
                            break
                except astroid.InferenceError:
                    pass
            self.add_message("using-constant-test", node=node)

    def visit_module(self, _: nodes.Module) -> None:
        """Check module name, docstring and required arguments."""
        self.linter.stats.node_count["module"] += 1

    def visit_classdef(self, _: nodes.ClassDef) -> None:
        """Check module name, docstring and redefinition
        increment branch counter
        """
        self.linter.stats.node_count["klass"] += 1

    @utils.check_messages(
        "pointless-statement", "pointless-string-statement", "expression-not-assigned"
    )
    def visit_expr(self, node: nodes.Expr) -> None:
        """Check for various kind of statements without effect."""
        expr = node.value
        if isinstance(expr, nodes.Const) and isinstance(expr.value, str):
            # treat string statement in a separated message
            # Handle PEP-257 attribute docstrings.
            # An attribute docstring is defined as being a string right after
            # an assignment at the module level, class level or __init__ level.
            scope = expr.scope()
            if isinstance(scope, (nodes.ClassDef, nodes.Module, nodes.FunctionDef)):
                if isinstance(scope, nodes.FunctionDef) and scope.name != "__init__":
                    pass
                else:
                    sibling = expr.previous_sibling()
                    if (
                        sibling is not None
                        and sibling.scope() is scope
                        and isinstance(sibling, (nodes.Assign, nodes.AnnAssign))
                    ):
                        return
            self.add_message("pointless-string-statement", node=node)
            return

        # Ignore if this is :
        # * a direct function call
        # * the unique child of a try/except body
        # * a yield statement
        # * an ellipsis (which can be used on Python 3 instead of pass)
        # warn W0106 if we have any underlying function call (we can't predict
        # side effects), else pointless-statement
        if (
            isinstance(expr, (nodes.Yield, nodes.Await, nodes.Call))
            or (isinstance(node.parent, nodes.TryExcept) and node.parent.body == [node])
            or (isinstance(expr, nodes.Const) and expr.value is Ellipsis)
        ):
            return
        if any(expr.nodes_of_class(nodes.Call)):
            self.add_message(
                "expression-not-assigned", node=node, args=expr.as_string()
            )
        else:
            self.add_message("pointless-statement", node=node)

    @staticmethod
    def _filter_vararg(node, call_args):
        # Return the arguments for the given call which are
        # not passed as vararg.
        for arg in call_args:
            if isinstance(arg, nodes.Starred):
                if (
                    isinstance(arg.value, nodes.Name)
                    and arg.value.name != node.args.vararg
                ):
                    yield arg
            else:
                yield arg

    @staticmethod
    def _has_variadic_argument(args, variadic_name):
        if not args:
            return True
        for arg in args:
            if isinstance(arg.value, nodes.Name):
                if arg.value.name != variadic_name:
                    return True
            else:
                return True
        return False

    @utils.check_messages("unnecessary-lambda")
    def visit_lambda(self, node: nodes.Lambda) -> None:
        """Check whether the lambda is suspicious."""
        # if the body of the lambda is a call expression with the same
        # argument list as the lambda itself, then the lambda is
        # possibly unnecessary and at least suspicious.
        if node.args.defaults:
            # If the arguments of the lambda include defaults, then a
            # judgment cannot be made because there is no way to check
            # that the defaults defined by the lambda are the same as
            # the defaults defined by the function called in the body
            # of the lambda.
            return
        call = node.body
        if not isinstance(call, nodes.Call):
            # The body of the lambda must be a function call expression
            # for the lambda to be unnecessary.
            return
        if isinstance(node.body.func, nodes.Attribute) and isinstance(
            node.body.func.expr, nodes.Call
        ):
            # Chained call, the intermediate call might
            # return something else (but we don't check that, yet).
            return

        call_site = astroid.arguments.CallSite.from_call(call)
        ordinary_args = list(node.args.args)
        new_call_args = list(self._filter_vararg(node, call.args))
        if node.args.kwarg:
            if self._has_variadic_argument(call.kwargs, node.args.kwarg):
                return

        if node.args.vararg:
            if self._has_variadic_argument(call.starargs, node.args.vararg):
                return
        elif call.starargs:
            return

        if call.keywords:
            # Look for additional keyword arguments that are not part
            # of the lambda's signature
            lambda_kwargs = {keyword.name for keyword in node.args.defaults}
            if len(lambda_kwargs) != len(call_site.keyword_arguments):
                # Different lengths, so probably not identical
                return
            if set(call_site.keyword_arguments).difference(lambda_kwargs):
                return

        # The "ordinary" arguments must be in a correspondence such that:
        # ordinary_args[i].name == call.args[i].name.
        if len(ordinary_args) != len(new_call_args):
            return
        for arg, passed_arg in zip(ordinary_args, new_call_args):
            if not isinstance(passed_arg, nodes.Name):
                return
            if arg.name != passed_arg.name:
                return

        self.add_message("unnecessary-lambda", line=node.fromlineno, node=node)

    @utils.check_messages("dangerous-default-value")
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Check function name, docstring, arguments, redefinition,
        variable names, max locals
        """
        if node.is_method():
            self.linter.stats.node_count["method"] += 1
        else:
            self.linter.stats.node_count["function"] += 1
        self._check_dangerous_default(node)

    visit_asyncfunctiondef = visit_functiondef

    def _check_dangerous_default(self, node):
        """Check for dangerous default values as arguments."""

        def is_iterable(internal_node):
            return isinstance(internal_node, (nodes.List, nodes.Set, nodes.Dict))

        defaults = node.args.defaults or [] + node.args.kw_defaults or []
        for default in defaults:
            if not default:
                continue
            try:
                value = next(default.infer())
            except astroid.InferenceError:
                continue

            if (
                isinstance(value, astroid.Instance)
                and value.qname() in DEFAULT_ARGUMENT_SYMBOLS
            ):
                if value is default:
                    msg = DEFAULT_ARGUMENT_SYMBOLS[value.qname()]
                elif isinstance(value, astroid.Instance) or is_iterable(value):
                    # We are here in the following situation(s):
                    #   * a dict/set/list/tuple call which wasn't inferred
                    #     to a syntax node ({}, () etc.). This can happen
                    #     when the arguments are invalid or unknown to
                    #     the inference.
                    #   * a variable from somewhere else, which turns out to be a list
                    #     or a dict.
                    if is_iterable(default):
                        msg = value.pytype()
                    elif isinstance(default, nodes.Call):
                        msg = f"{value.name}() ({value.qname()})"
                    else:
                        msg = f"{default.as_string()} ({value.qname()})"
                else:
                    # this argument is a name
                    msg = f"{default.as_string()} ({DEFAULT_ARGUMENT_SYMBOLS[value.qname()]})"
                self.add_message("dangerous-default-value", node=node, args=(msg,))

    @utils.check_messages("unreachable", "lost-exception")
    def visit_return(self, node: nodes.Return) -> None:
        """Return node visitor.

        1 - check if the node has a right sibling (if so, that's some
        unreachable code)
        2 - check if the node is inside the 'finally' clause of a 'try...finally'
        block
        """
        self._check_unreachable(node)
        # Is it inside final body of a try...finally block ?
        self._check_not_in_finally(node, "return", (nodes.FunctionDef,))

    @utils.check_messages("unreachable")
    def visit_continue(self, node: nodes.Continue) -> None:
        """Check is the node has a right sibling (if so, that's some unreachable
        code)
        """
        self._check_unreachable(node)

    @utils.check_messages("unreachable", "lost-exception")
    def visit_break(self, node: nodes.Break) -> None:
        """Break node visitor.

        1 - check if the node has a right sibling (if so, that's some
        unreachable code)
        2 - check if the node is inside the 'finally' clause of a 'try...finally'
        block
        """
        # 1 - Is it right sibling ?
        self._check_unreachable(node)
        # 2 - Is it inside final body of a try...finally block ?
        self._check_not_in_finally(node, "break", (nodes.For, nodes.While))

    @utils.check_messages("unreachable")
    def visit_raise(self, node: nodes.Raise) -> None:
        """Check if the node has a right sibling (if so, that's some unreachable
        code)
        """
        self._check_unreachable(node)

    def _check_misplaced_format_function(self, call_node):
        if not isinstance(call_node.func, nodes.Attribute):
            return
        if call_node.func.attrname != "format":
            return

        expr = utils.safe_infer(call_node.func.expr)
        if expr is astroid.Uninferable:
            return
        if not expr:
            # we are doubtful on inferred type of node, so here just check if format
            # was called on print()
            call_expr = call_node.func.expr
            if not isinstance(call_expr, nodes.Call):
                return
            if (
                isinstance(call_expr.func, nodes.Name)
                and call_expr.func.name == "print"
            ):
                self.add_message("misplaced-format-function", node=call_node)

    @utils.check_messages(
        "eval-used", "exec-used", "bad-reversed-sequence", "misplaced-format-function"
    )
    def visit_call(self, node: nodes.Call) -> None:
        """Visit a Call node -> check if this is not a disallowed builtin
        call and check for * or ** use
        """
        self._check_misplaced_format_function(node)
        if isinstance(node.func, nodes.Name):
            name = node.func.name
            # ignore the name if it's not a builtin (i.e. not defined in the
            # locals nor globals scope)
            if not (name in node.frame(future=True) or name in node.root()):
                if name == "exec":
                    self.add_message("exec-used", node=node)
                elif name == "reversed":
                    self._check_reversed(node)
                elif name == "eval":
                    self.add_message("eval-used", node=node)

    @utils.check_messages("assert-on-tuple", "assert-on-string-literal")
    def visit_assert(self, node: nodes.Assert) -> None:
        """Check whether assert is used on a tuple or string literal."""
        if (
            node.fail is None
            and isinstance(node.test, nodes.Tuple)
            and len(node.test.elts) == 2
        ):
            self.add_message("assert-on-tuple", node=node)

        if isinstance(node.test, nodes.Const) and isinstance(node.test.value, str):
            if node.test.value:
                when = "never"
            else:
                when = "always"
            self.add_message("assert-on-string-literal", node=node, args=(when,))

    @utils.check_messages("duplicate-key")
    def visit_dict(self, node: nodes.Dict) -> None:
        """Check duplicate key in dictionary."""
        keys = set()
        for k, _ in node.items:
            if isinstance(k, nodes.Const):
                key = k.value
            elif isinstance(k, nodes.Attribute):
                key = k.as_string()
            else:
                continue
            if key in keys:
                self.add_message("duplicate-key", node=node, args=key)
            keys.add(key)

    def visit_tryfinally(self, node: nodes.TryFinally) -> None:
        """Update try...finally flag."""
        self._tryfinallys.append(node)

    def leave_tryfinally(self, _: nodes.TryFinally) -> None:
        """Update try...finally flag."""
        self._tryfinallys.pop()

    def _check_unreachable(self, node):
        """Check unreachable code."""
        unreach_stmt = node.next_sibling()
        if unreach_stmt is not None:
            if (
                isinstance(node, nodes.Return)
                and isinstance(unreach_stmt, nodes.Expr)
                and isinstance(unreach_stmt.value, nodes.Yield)
            ):
                # Don't add 'unreachable' for empty generators.
                # Only add warning if 'yield' is followed by another node.
                unreach_stmt = unreach_stmt.next_sibling()
                if unreach_stmt is None:
                    return
            self.add_message("unreachable", node=unreach_stmt)

    def _check_not_in_finally(self, node, node_name, breaker_classes=()):
        """Check that a node is not inside a 'finally' clause of a
        'try...finally' statement.

        If we find a parent which type is in breaker_classes before
        a 'try...finally' block we skip the whole check.
        """
        # if self._tryfinallys is empty, we're not an in try...finally block
        if not self._tryfinallys:
            return
        # the node could be a grand-grand...-child of the 'try...finally'
        _parent = node.parent
        _node = node
        while _parent and not isinstance(_parent, breaker_classes):
            if hasattr(_parent, "finalbody") and _node in _parent.finalbody:
                self.add_message("lost-exception", node=node, args=node_name)
                return
            _node = _parent
            _parent = _node.parent

    def _check_reversed(self, node):
        """Check that the argument to `reversed` is a sequence."""
        try:
            argument = utils.safe_infer(utils.get_argument_from_call(node, position=0))
        except utils.NoSuchArgumentError:
            pass
        else:
            if argument is astroid.Uninferable:
                return
            if argument is None:
                # Nothing was inferred.
                # Try to see if we have iter().
                if isinstance(node.args[0], nodes.Call):
                    try:
                        func = next(node.args[0].func.infer())
                    except astroid.InferenceError:
                        return
                    if getattr(
                        func, "name", None
                    ) == "iter" and utils.is_builtin_object(func):
                        self.add_message("bad-reversed-sequence", node=node)
                return

            if isinstance(argument, (nodes.List, nodes.Tuple)):
                return

            # dicts are reversible, but only from Python 3.8 onwards. Prior to
            # that, any class based on dict must explicitly provide a
            # __reversed__ method
            if not self._py38_plus and isinstance(argument, astroid.Instance):
                if any(
                    ancestor.name == "dict" and utils.is_builtin_object(ancestor)
                    for ancestor in itertools.chain(
                        (argument._proxied,), argument._proxied.ancestors()
                    )
                ):
                    try:
                        argument.locals[REVERSED_PROTOCOL_METHOD]
                    except KeyError:
                        self.add_message("bad-reversed-sequence", node=node)
                    return

            if hasattr(argument, "getattr"):
                # everything else is not a proper sequence for reversed()
                for methods in REVERSED_METHODS:
                    for meth in methods:
                        try:
                            argument.getattr(meth)
                        except astroid.NotFoundError:
                            break
                    else:
                        break
                else:
                    self.add_message("bad-reversed-sequence", node=node)
            else:
                self.add_message("bad-reversed-sequence", node=node)

    @utils.check_messages("confusing-with-statement")
    def visit_with(self, node: nodes.With) -> None:
        # a "with" statement with multiple managers corresponds
        # to one AST "With" node with multiple items
        pairs = node.items
        if pairs:
            for prev_pair, pair in zip(pairs, pairs[1:]):
                if isinstance(prev_pair[1], nodes.AssignName) and (
                    pair[1] is None and not isinstance(pair[0], nodes.Call)
                ):
                    # Don't emit a message if the second is a function call
                    # there's no way that can be mistaken for a name assignment.
                    # If the line number doesn't match
                    # we assume it's a nested "with".
                    self.add_message("confusing-with-statement", node=node)

    def _check_self_assigning_variable(self, node):
        # Detect assigning to the same variable.

        scope = node.scope()
        scope_locals = scope.locals

        rhs_names = []
        targets = node.targets
        if isinstance(targets[0], nodes.Tuple):
            if len(targets) != 1:
                # A complex assignment, so bail out early.
                return
            targets = targets[0].elts
            if len(targets) == 1:
                # Unpacking a variable into the same name.
                return

        if isinstance(node.value, nodes.Name):
            if len(targets) != 1:
                return
            rhs_names = [node.value]
        elif isinstance(node.value, nodes.Tuple):
            rhs_count = len(node.value.elts)
            if len(targets) != rhs_count or rhs_count == 1:
                return
            rhs_names = node.value.elts

        for target, lhs_name in zip(targets, rhs_names):
            if not isinstance(lhs_name, nodes.Name):
                continue
            if not isinstance(target, nodes.AssignName):
                continue
            # Check that the scope is different from a class level, which is usually
            # a pattern to expose module level attributes as class level ones.
            if isinstance(scope, nodes.ClassDef) and target.name in scope_locals:
                continue
            if target.name == lhs_name.name:
                self.add_message(
                    "self-assigning-variable", args=(target.name,), node=target
                )

    def _check_redeclared_assign_name(self, targets):
        dummy_variables_rgx = lint_utils.get_global_option(
            self, "dummy-variables-rgx", default=None
        )

        for target in targets:
            if not isinstance(target, nodes.Tuple):
                continue

            found_names = []
            for element in target.elts:
                if isinstance(element, nodes.Tuple):
                    self._check_redeclared_assign_name([element])
                elif isinstance(element, nodes.AssignName) and element.name != "_":
                    if dummy_variables_rgx and dummy_variables_rgx.match(element.name):
                        return
                    found_names.append(element.name)

            names = collections.Counter(found_names)
            for name, count in names.most_common():
                if count > 1:
                    self.add_message(
                        "redeclared-assigned-name", args=(name,), node=target
                    )

    @utils.check_messages("self-assigning-variable", "redeclared-assigned-name")
    def visit_assign(self, node: nodes.Assign) -> None:
        self._check_self_assigning_variable(node)
        self._check_redeclared_assign_name(node.targets)

    @utils.check_messages("redeclared-assigned-name")
    def visit_for(self, node: nodes.For) -> None:
        self._check_redeclared_assign_name([node.target])


def register(linter: "PyLinter") -> None:
    linter.register_checker(BasicErrorChecker(linter))
    linter.register_checker(BasicChecker(linter))
    linter.register_checker(NameChecker(linter))
    linter.register_checker(DocStringChecker(linter))
    linter.register_checker(PassChecker(linter))
    linter.register_checker(ComparisonChecker(linter))
