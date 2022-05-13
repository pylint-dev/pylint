# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Variables checkers for Python code."""
import collections
import copy
import itertools
import os
import re
import sys
from enum import Enum
from functools import lru_cache
from typing import (
    TYPE_CHECKING,
    Any,
    DefaultDict,
    Dict,
    Iterable,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    Union,
)

import astroid
from astroid import nodes

from pylint.checkers import BaseChecker, utils
from pylint.checkers.utils import (
    in_type_checking_block,
    is_postponed_evaluation_enabled,
)
from pylint.constants import PY39_PLUS, TYPING_TYPE_CHECKS_GUARDS
from pylint.interfaces import (
    CONTROL_FLOW,
    HIGH,
    INFERENCE,
    INFERENCE_FAILURE,
    IAstroidChecker,
)
from pylint.utils import get_global_option

if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    from astroid.decorators import cachedproperty as cached_property

if TYPE_CHECKING:
    from pylint.lint import PyLinter

SPECIAL_OBJ = re.compile("^_{2}[a-z]+_{2}$")
FUTURE = "__future__"
# regexp for ignored argument name
IGNORED_ARGUMENT_NAMES = re.compile("_.*|^ignored_|^unused_")
# In Python 3.7 abc has a Python implementation which is preferred
# by astroid. Unfortunately this also messes up our explicit checks
# for `abc`
METACLASS_NAME_TRANSFORMS = {"_py_abc": "abc"}
BUILTIN_RANGE = "builtins.range"
TYPING_MODULE = "typing"
TYPING_NAMES = frozenset(
    {
        "Any",
        "Callable",
        "ClassVar",
        "Generic",
        "Optional",
        "Tuple",
        "Type",
        "TypeVar",
        "Union",
        "AbstractSet",
        "ByteString",
        "Container",
        "ContextManager",
        "Hashable",
        "ItemsView",
        "Iterable",
        "Iterator",
        "KeysView",
        "Mapping",
        "MappingView",
        "MutableMapping",
        "MutableSequence",
        "MutableSet",
        "Sequence",
        "Sized",
        "ValuesView",
        "Awaitable",
        "AsyncIterator",
        "AsyncIterable",
        "Coroutine",
        "Collection",
        "AsyncGenerator",
        "AsyncContextManager",
        "Reversible",
        "SupportsAbs",
        "SupportsBytes",
        "SupportsComplex",
        "SupportsFloat",
        "SupportsInt",
        "SupportsRound",
        "Counter",
        "Deque",
        "Dict",
        "DefaultDict",
        "List",
        "Set",
        "FrozenSet",
        "NamedTuple",
        "Generator",
        "AnyStr",
        "Text",
        "Pattern",
        "BinaryIO",
    }
)


class VariableVisitConsumerAction(Enum):
    """Reported by _check_consumer() and its sub-methods to determine the
    subsequent action to take in _undefined_and_used_before_checker().

    Continue -> continue loop to next consumer
    Return -> return and thereby break the loop
    """

    CONTINUE = 0
    RETURN = 1


def _is_from_future_import(stmt, name):
    """Check if the name is a future import from another module."""
    try:
        module = stmt.do_import_module(stmt.modname)
    except astroid.AstroidBuildingException:
        return None

    for local_node in module.locals.get(name, []):
        if isinstance(local_node, nodes.ImportFrom) and local_node.modname == FUTURE:
            return True
    return None


def in_for_else_branch(parent, stmt):
    """Returns True if stmt in inside the else branch for a parent For stmt."""
    return isinstance(parent, nodes.For) and any(
        else_stmt.parent_of(stmt) or else_stmt == stmt for else_stmt in parent.orelse
    )


@lru_cache(maxsize=1000)
def overridden_method(klass, name):
    """Get overridden method if any."""
    try:
        parent = next(klass.local_attr_ancestors(name))
    except (StopIteration, KeyError):
        return None
    try:
        meth_node = parent[name]
    except KeyError:
        # We have found an ancestor defining <name> but it's not in the local
        # dictionary. This may happen with astroid built from living objects.
        return None
    if isinstance(meth_node, nodes.FunctionDef):
        return meth_node
    return None


def _get_unpacking_extra_info(node, inferred):
    """Return extra information to add to the message for unpacking-non-sequence
    and unbalanced-tuple-unpacking errors
    """
    more = ""
    inferred_module = inferred.root().name
    if node.root().name == inferred_module:
        if node.lineno == inferred.lineno:
            more = f" {inferred.as_string()}"
        elif inferred.lineno:
            more = f" defined at line {inferred.lineno}"
    elif inferred.lineno:
        more = f" defined at line {inferred.lineno} of {inferred_module}"
    return more


def _detect_global_scope(node, frame, defframe):
    """Detect that the given frames share a global scope.

    Two frames share a global scope when neither
    of them are hidden under a function scope, as well
    as any parent scope of them, until the root scope.
    In this case, depending from something defined later on
    will only work if guarded by a nested function definition.

    Example:
        class A:
            # B has the same global scope as `C`, leading to a NameError.
            # Return True to indicate a shared scope.
            class B(C): ...
        class C: ...

    Whereas this does not lead to a NameError:
        class A:
            def guard():
                # Return False to indicate no scope sharing.
                class B(C): ...
        class C: ...
    """
    def_scope = scope = None
    if frame and frame.parent:
        scope = frame.parent.scope()
    if defframe and defframe.parent:
        def_scope = defframe.parent.scope()
    if (
        isinstance(frame, nodes.ClassDef)
        and scope is not def_scope
        and scope is utils.get_node_first_ancestor_of_type(node, nodes.FunctionDef)
    ):
        # If the current node's scope is a class nested under a function,
        # and the def_scope is something else, then they aren't shared.
        return False
    if isinstance(frame, nodes.FunctionDef):
        # If the parent of the current node is a
        # function, then it can be under its scope
        # (defined in, which doesn't concern us) or
        # the `->` part of annotations. The same goes
        # for annotations of function arguments, they'll have
        # their parent the Arguments node.
        if not isinstance(node.parent, (nodes.FunctionDef, nodes.Arguments)):
            return False
    elif any(
        not isinstance(f, (nodes.ClassDef, nodes.Module)) for f in (frame, defframe)
    ):
        # Not interested in other frames, since they are already
        # not in a global scope.
        return False

    break_scopes = []
    for current_scope in (scope, def_scope):
        # Look for parent scopes. If there is anything different
        # than a module or a class scope, then they frames don't
        # share a global scope.
        parent_scope = current_scope
        while parent_scope:
            if not isinstance(parent_scope, (nodes.ClassDef, nodes.Module)):
                break_scopes.append(parent_scope)
                break
            if parent_scope.parent:
                parent_scope = parent_scope.parent.scope()
            else:
                break
    if break_scopes and len(set(break_scopes)) != 1:
        # Store different scopes than expected.
        # If the stored scopes are, in fact, the very same, then it means
        # that the two frames (frame and defframe) share the same scope,
        # and we could apply our lineno analysis over them.
        # For instance, this works when they are inside a function, the node
        # that uses a definition and the definition itself.
        return False
    # At this point, we are certain that frame and defframe share a scope
    # and the definition of the first depends on the second.
    return frame.lineno < defframe.lineno


def _infer_name_module(node, name):
    context = astroid.context.InferenceContext()
    context.lookupname = name
    return node.infer(context, asname=False)


def _fix_dot_imports(not_consumed):
    """Try to fix imports with multiple dots, by returning a dictionary
    with the import names expanded.

    The function unflattens root imports,
    like 'xml' (when we have both 'xml.etree' and 'xml.sax'), to 'xml.etree'
    and 'xml.sax' respectively.
    """
    names = {}
    for name, stmts in not_consumed.items():
        if any(
            isinstance(stmt, nodes.AssignName)
            and isinstance(stmt.assign_type(), nodes.AugAssign)
            for stmt in stmts
        ):
            continue
        for stmt in stmts:
            if not isinstance(stmt, (nodes.ImportFrom, nodes.Import)):
                continue
            for imports in stmt.names:
                second_name = None
                import_module_name = imports[0]
                if import_module_name == "*":
                    # In case of wildcard imports,
                    # pick the name from inside the imported module.
                    second_name = name
                else:
                    name_matches_dotted_import = False
                    if (
                        import_module_name.startswith(name)
                        and import_module_name.find(".") > -1
                    ):
                        name_matches_dotted_import = True

                    if name_matches_dotted_import or name in imports:
                        # Most likely something like 'xml.etree',
                        # which will appear in the .locals as 'xml'.
                        # Only pick the name if it wasn't consumed.
                        second_name = import_module_name
                if second_name and second_name not in names:
                    names[second_name] = stmt
    return sorted(names.items(), key=lambda a: a[1].fromlineno)


def _find_frame_imports(name, frame):
    """Detect imports in the frame, with the required *name*.

    Such imports can be considered assignments.
    Returns True if an import for the given name was found.
    """
    imports = frame.nodes_of_class((nodes.Import, nodes.ImportFrom))
    for import_node in imports:
        for import_name, import_alias in import_node.names:
            # If the import uses an alias, check only that.
            # Otherwise, check only the import name.
            if import_alias:
                if import_alias == name:
                    return True
            elif import_name and import_name == name:
                return True
    return None


def _import_name_is_global(stmt, global_names):
    for import_name, import_alias in stmt.names:
        # If the import uses an alias, check only that.
        # Otherwise, check only the import name.
        if import_alias:
            if import_alias in global_names:
                return True
        elif import_name in global_names:
            return True
    return False


def _flattened_scope_names(
    iterator: Iterator[Union[nodes.Global, nodes.Nonlocal]]
) -> Set[str]:
    values = (set(stmt.names) for stmt in iterator)
    return set(itertools.chain.from_iterable(values))


def _assigned_locally(name_node):
    """Checks if name_node has corresponding assign statement in same scope."""
    assign_stmts = name_node.scope().nodes_of_class(nodes.AssignName)
    return any(a.name == name_node.name for a in assign_stmts)


def _has_locals_call_after_node(stmt, scope):
    skip_nodes = (
        nodes.FunctionDef,
        nodes.ClassDef,
        nodes.Import,
        nodes.ImportFrom,
    )
    for call in scope.nodes_of_class(nodes.Call, skip_klass=skip_nodes):
        inferred = utils.safe_infer(call.func)
        if (
            utils.is_builtin_object(inferred)
            and getattr(inferred, "name", None) == "locals"
        ):
            if stmt.lineno < call.lineno:
                return True
    return False


MSGS = {
    "E0601": (
        "Using variable %r before assignment",
        "used-before-assignment",
        "Emitted when a local variable is accessed before its assignment took place. "
        "Assignments in try blocks are assumed not to have occurred when evaluating "
        "associated except/finally blocks. Assignments in except blocks are assumed "
        "not to have occurred when evaluating statements outside the block, except "
        "when the associated try block contains a return statement.",
    ),
    "E0602": (
        "Undefined variable %r",
        "undefined-variable",
        "Used when an undefined variable is accessed.",
    ),
    "E0603": (
        "Undefined variable name %r in __all__",
        "undefined-all-variable",
        "Used when an undefined variable name is referenced in __all__.",
    ),
    "E0604": (
        "Invalid object %r in __all__, must contain only strings",
        "invalid-all-object",
        "Used when an invalid (non-string) object occurs in __all__.",
    ),
    "E0605": (
        "Invalid format for __all__, must be tuple or list",
        "invalid-all-format",
        "Used when __all__ has an invalid format.",
    ),
    "E0611": (
        "No name %r in module %r",
        "no-name-in-module",
        "Used when a name cannot be found in a module.",
    ),
    "W0601": (
        "Global variable %r undefined at the module level",
        "global-variable-undefined",
        'Used when a variable is defined through the "global" statement '
        "but the variable is not defined in the module scope.",
    ),
    "W0602": (
        "Using global for %r but no assignment is done",
        "global-variable-not-assigned",
        'Used when a variable is defined through the "global" statement '
        "but no assignment to this variable is done.",
    ),
    "W0603": (
        "Using the global statement",  # W0121
        "global-statement",
        'Used when you use the "global" statement to update a global '
        "variable. Pylint just try to discourage this "
        "usage. That doesn't mean you cannot use it !",
    ),
    "W0604": (
        "Using the global statement at the module level",  # W0103
        "global-at-module-level",
        'Used when you use the "global" statement at the module level '
        "since it has no effect",
    ),
    "W0611": (
        "Unused %s",
        "unused-import",
        "Used when an imported module or variable is not used.",
    ),
    "W0612": (
        "Unused variable %r",
        "unused-variable",
        "Used when a variable is defined but not used.",
    ),
    "W0613": (
        "Unused argument %r",
        "unused-argument",
        "Used when a function or method argument is not used.",
    ),
    "W0614": (
        "Unused import(s) %s from wildcard import of %s",
        "unused-wildcard-import",
        "Used when an imported module or variable is not used from a "
        "`'from X import *'` style import.",
    ),
    "W0621": (
        "Redefining name %r from outer scope (line %s)",
        "redefined-outer-name",
        "Used when a variable's name hides a name defined in the outer scope.",
    ),
    "W0622": (
        "Redefining built-in %r",
        "redefined-builtin",
        "Used when a variable or function override a built-in.",
    ),
    "W0631": (
        "Using possibly undefined loop variable %r",
        "undefined-loop-variable",
        "Used when a loop variable (i.e. defined by a for loop or "
        "a list comprehension or a generator expression) is used outside "
        "the loop.",
    ),
    "W0632": (
        "Possible unbalanced tuple unpacking with "
        "sequence%s: "
        "left side has %d label(s), right side has %d value(s)",
        "unbalanced-tuple-unpacking",
        "Used when there is an unbalanced tuple unpacking in assignment",
        {"old_names": [("E0632", "old-unbalanced-tuple-unpacking")]},
    ),
    "E0633": (
        "Attempting to unpack a non-sequence%s",
        "unpacking-non-sequence",
        "Used when something which is not "
        "a sequence is used in an unpack assignment",
        {"old_names": [("W0633", "old-unpacking-non-sequence")]},
    ),
    "W0640": (
        "Cell variable %s defined in loop",
        "cell-var-from-loop",
        "A variable used in a closure is defined in a loop. "
        "This will result in all closures using the same value for "
        "the closed-over variable.",
    ),
    "W0641": (
        "Possibly unused variable %r",
        "possibly-unused-variable",
        "Used when a variable is defined but might not be used. "
        "The possibility comes from the fact that locals() might be used, "
        "which could consume or not the said variable",
    ),
    "W0642": (
        "Invalid assignment to %s in method",
        "self-cls-assignment",
        "Invalid assignment to self or cls in instance or class method "
        "respectively.",
    ),
}


class ScopeConsumer(NamedTuple):
    """Store nodes and their consumption states."""

    to_consume: Dict[str, List[nodes.NodeNG]]
    consumed: Dict[str, List[nodes.NodeNG]]
    consumed_uncertain: DefaultDict[str, List[nodes.NodeNG]]
    scope_type: str


class NamesConsumer:
    """A simple class to handle consumed, to consume and scope type info of node locals."""

    def __init__(self, node, scope_type):
        self._atomic = ScopeConsumer(
            copy.copy(node.locals), {}, collections.defaultdict(list), scope_type
        )
        self.node = node

    def __repr__(self):
        to_consumes = [f"{k}->{v}" for k, v in self._atomic.to_consume.items()]
        consumed = [f"{k}->{v}" for k, v in self._atomic.consumed.items()]
        consumed_uncertain = [
            f"{k}->{v}" for k, v in self._atomic.consumed_uncertain.items()
        ]
        to_consumes = ", ".join(to_consumes)
        consumed = ", ".join(consumed)
        consumed_uncertain = ", ".join(consumed_uncertain)
        return f"""
to_consume : {to_consumes}
consumed : {consumed}
consumed_uncertain: {consumed_uncertain}
scope_type : {self._atomic.scope_type}
"""

    def __iter__(self):
        return iter(self._atomic)

    @property
    def to_consume(self):
        return self._atomic.to_consume

    @property
    def consumed(self):
        return self._atomic.consumed

    @property
    def consumed_uncertain(self) -> DefaultDict[str, List[nodes.NodeNG]]:
        """Retrieves nodes filtered out by get_next_to_consume() that may not
        have executed, such as statements in except blocks, or statements

        in try blocks (when evaluating their corresponding except and finally
        blocks). Checkers that want to treat the statements as executed
        (e.g. for unused-variable) may need to add them back.
        """
        return self._atomic.consumed_uncertain

    @property
    def scope_type(self):
        return self._atomic.scope_type

    def mark_as_consumed(self, name, consumed_nodes):
        """Mark the given nodes as consumed for the name.

        If all of the nodes for the name were consumed, delete the name from
        the to_consume dictionary
        """
        unconsumed = [n for n in self.to_consume[name] if n not in set(consumed_nodes)]
        self.consumed[name] = consumed_nodes

        if unconsumed:
            self.to_consume[name] = unconsumed
        else:
            del self.to_consume[name]

    def get_next_to_consume(self, node: nodes.Name) -> Optional[List[nodes.NodeNG]]:
        """Return a list of the nodes that define `node` from this scope.

        If it is uncertain whether a node will be consumed, such as for statements in
        except blocks, add it to self.consumed_uncertain instead of returning it.
        Return None to indicate a special case that needs to be handled by the caller.
        """
        name = node.name
        parent_node = node.parent
        found_nodes = self.to_consume.get(name)
        node_statement = node.statement(future=True)
        if (
            found_nodes
            and isinstance(parent_node, nodes.Assign)
            and parent_node == found_nodes[0].parent
        ):
            lhs = found_nodes[0].parent.targets[0]
            if lhs.name == name:  # this name is defined in this very statement
                found_nodes = None

        if (
            found_nodes
            and isinstance(parent_node, nodes.For)
            and parent_node.iter == node
            and parent_node.target in found_nodes
        ):
            found_nodes = None

        # Before filtering, check that this node's name is not a nonlocal
        if any(
            isinstance(child, nodes.Nonlocal) and node.name in child.names
            for child in node.frame(future=True).get_children()
        ):
            return found_nodes

        # And no comprehension is under the node's frame
        if VariablesChecker._comprehension_between_frame_and_node(node):
            return found_nodes

        # Filter out assignments in ExceptHandlers that node is not contained in
        if found_nodes:
            found_nodes = [
                n
                for n in found_nodes
                if not isinstance(n.statement(future=True), nodes.ExceptHandler)
                or n.statement(future=True).parent_of(node)
            ]

        # Filter out assignments in an Except clause that the node is not
        # contained in, assuming they may fail
        if found_nodes:
            uncertain_nodes = self._uncertain_nodes_in_except_blocks(
                found_nodes, node, node_statement
            )
            self.consumed_uncertain[node.name] += uncertain_nodes
            uncertain_nodes_set = set(uncertain_nodes)
            found_nodes = [n for n in found_nodes if n not in uncertain_nodes_set]

        # If this node is in a Finally block of a Try/Finally,
        # filter out assignments in the try portion, assuming they may fail
        if found_nodes:
            uncertain_nodes = (
                self._uncertain_nodes_in_try_blocks_when_evaluating_finally_blocks(
                    found_nodes, node_statement
                )
            )
            self.consumed_uncertain[node.name] += uncertain_nodes
            uncertain_nodes_set = set(uncertain_nodes)
            found_nodes = [n for n in found_nodes if n not in uncertain_nodes_set]

        # If this node is in an ExceptHandler,
        # filter out assignments in the try portion, assuming they may fail
        if found_nodes:
            uncertain_nodes = (
                self._uncertain_nodes_in_try_blocks_when_evaluating_except_blocks(
                    found_nodes, node_statement
                )
            )
            self.consumed_uncertain[node.name] += uncertain_nodes
            uncertain_nodes_set = set(uncertain_nodes)
            found_nodes = [n for n in found_nodes if n not in uncertain_nodes_set]

        return found_nodes

    @staticmethod
    def _uncertain_nodes_in_except_blocks(
        found_nodes: List[nodes.NodeNG],
        node: nodes.NodeNG,
        node_statement: nodes.Statement,
    ) -> List[nodes.NodeNG]:
        """Return any nodes in ``found_nodes`` that should be treated as uncertain
        because they are in an except block.
        """
        uncertain_nodes = []
        for other_node in found_nodes:
            other_node_statement = other_node.statement(future=True)
            # Only testing for statements in the except block of TryExcept
            closest_except_handler = utils.get_node_first_ancestor_of_type(
                other_node_statement, nodes.ExceptHandler
            )
            if not closest_except_handler:
                continue
            # If the other node is in the same scope as this node, assume it executes
            if closest_except_handler.parent_of(node):
                continue
            closest_try_except: nodes.TryExcept = closest_except_handler.parent
            try_block_returns = any(
                isinstance(try_statement, nodes.Return)
                for try_statement in closest_try_except.body
            )
            # If the try block returns, assume the except blocks execute.
            if try_block_returns:
                # Exception: if this node is in the final block of the other_node_statement,
                # it will execute before returning. Assume the except statements are uncertain.
                if (
                    isinstance(node_statement.parent, nodes.TryFinally)
                    and node_statement in node_statement.parent.finalbody
                    and closest_try_except.parent.parent_of(node_statement)
                ):
                    uncertain_nodes.append(other_node)
                # Assume the except blocks execute, so long as each handler
                # defines the name, raises, or returns.
                elif all(
                    NamesConsumer._defines_name_raises_or_returns(node.name, handler)
                    for handler in closest_try_except.handlers
                ):
                    continue

            if NamesConsumer._check_loop_finishes_via_except(node, closest_try_except):
                continue

            # Passed all tests for uncertain execution
            uncertain_nodes.append(other_node)
        return uncertain_nodes

    @staticmethod
    def _defines_name_raises_or_returns(
        name: str, handler: nodes.ExceptHandler
    ) -> bool:
        """Return True if some child of `handler` defines the name `name`,
        raises, or returns.
        """

        def _define_raise_or_return(stmt: nodes.NodeNG) -> bool:
            if isinstance(stmt, (nodes.Raise, nodes.Return)):
                return True
            if isinstance(stmt, nodes.Assign):
                for target in stmt.targets:
                    for elt in utils.get_all_elements(target):
                        if isinstance(elt, nodes.AssignName) and elt.name == name:
                            return True
            if isinstance(stmt, nodes.If):
                # Check for assignments inside the test
                if (
                    isinstance(stmt.test, nodes.NamedExpr)
                    and stmt.test.target.name == name
                ):
                    return True
                if isinstance(stmt.test, nodes.Call):
                    for arg_or_kwarg in stmt.test.args + [
                        kw.value for kw in stmt.test.keywords
                    ]:
                        if (
                            isinstance(arg_or_kwarg, nodes.NamedExpr)
                            and arg_or_kwarg.target.name == name
                        ):
                            return True
            return False

        for stmt in handler.get_children():
            if _define_raise_or_return(stmt):
                return True
            if isinstance(stmt, (nodes.If, nodes.With)):
                if any(
                    _define_raise_or_return(nested_stmt)
                    for nested_stmt in stmt.get_children()
                ):
                    return True
        return False

    @staticmethod
    def _check_loop_finishes_via_except(
        node: nodes.NodeNG, other_node_try_except: nodes.TryExcept
    ) -> bool:
        """Check for a case described in https://github.com/PyCQA/pylint/issues/5683.

        It consists of a specific control flow scenario where the only
        non-break exit from a loop consists of the very except handler we are
        examining, such that code in the `else` branch of the loop can depend on it
        being assigned.

        Example:

        for _ in range(3):
            try:
                do_something()
            except:
                name = 1  <-- only non-break exit from loop
            else:
                break
        else:
            print(name)
        """
        if not other_node_try_except.orelse:
            return False
        closest_loop: Optional[
            Union[nodes.For, nodes.While]
        ] = utils.get_node_first_ancestor_of_type(node, (nodes.For, nodes.While))
        if closest_loop is None:
            return False
        if not any(
            else_statement is node or else_statement.parent_of(node)
            for else_statement in closest_loop.orelse
        ):
            # `node` not guarded by `else`
            return False
        for inner_else_statement in other_node_try_except.orelse:
            if isinstance(inner_else_statement, nodes.Break):
                break_stmt = inner_else_statement
                break
        else:
            # No break statement
            return False

        def _try_in_loop_body(
            other_node_try_except: nodes.TryExcept, loop: Union[nodes.For, nodes.While]
        ) -> bool:
            """Return True if `other_node_try_except` is a descendant of `loop`."""
            return any(
                loop_body_statement is other_node_try_except
                or loop_body_statement.parent_of(other_node_try_except)
                for loop_body_statement in loop.body
            )

        if not _try_in_loop_body(other_node_try_except, closest_loop):
            for ancestor in closest_loop.node_ancestors():
                if isinstance(ancestor, (nodes.For, nodes.While)):
                    if _try_in_loop_body(other_node_try_except, ancestor):
                        break
            else:
                # `other_node_try_except` didn't have a shared ancestor loop
                return False

        for loop_stmt in closest_loop.body:
            if NamesConsumer._recursive_search_for_continue_before_break(
                loop_stmt, break_stmt
            ):
                break
        else:
            # No continue found, so we arrived at our special case!
            return True
        return False

    @staticmethod
    def _recursive_search_for_continue_before_break(
        stmt: nodes.Statement, break_stmt: nodes.Break
    ) -> bool:
        """Return True if any Continue node can be found in descendants of `stmt`
        before encountering `break_stmt`, ignoring any nested loops.
        """
        if stmt is break_stmt:
            return False
        if isinstance(stmt, nodes.Continue):
            return True
        for child in stmt.get_children():
            if isinstance(stmt, (nodes.For, nodes.While)):
                continue
            if NamesConsumer._recursive_search_for_continue_before_break(
                child, break_stmt
            ):
                return True
        return False

    @staticmethod
    def _uncertain_nodes_in_try_blocks_when_evaluating_except_blocks(
        found_nodes: List[nodes.NodeNG], node_statement: nodes.Statement
    ) -> List[nodes.NodeNG]:
        """Return any nodes in ``found_nodes`` that should be treated as uncertain because they
        are in a try block and the ``node_statement`` being evaluated is in one of its except handlers.
        """
        uncertain_nodes: List[nodes.NodeNG] = []
        closest_except_handler = utils.get_node_first_ancestor_of_type(
            node_statement, nodes.ExceptHandler
        )
        if closest_except_handler is None:
            return uncertain_nodes
        for other_node in found_nodes:
            other_node_statement = other_node.statement(future=True)
            # If the other statement is the except handler guarding `node`, it executes
            if other_node_statement is closest_except_handler:
                continue
            # Ensure other_node is in a try block
            (
                other_node_try_ancestor,
                other_node_try_ancestor_visited_child,
            ) = utils.get_node_first_ancestor_of_type_and_its_child(
                other_node_statement, nodes.TryExcept
            )
            if other_node_try_ancestor is None:
                continue
            if (
                other_node_try_ancestor_visited_child
                not in other_node_try_ancestor.body
            ):
                continue
            # Make sure nesting is correct -- there should be at least one
            # except handler that is a sibling attached to the try ancestor,
            # or is an ancestor of the try ancestor.
            if not any(
                closest_except_handler in other_node_try_ancestor.handlers
                or other_node_try_ancestor_except_handler
                in closest_except_handler.node_ancestors()
                for other_node_try_ancestor_except_handler in other_node_try_ancestor.handlers
            ):
                continue
            # Passed all tests for uncertain execution
            uncertain_nodes.append(other_node)
        return uncertain_nodes

    @staticmethod
    def _uncertain_nodes_in_try_blocks_when_evaluating_finally_blocks(
        found_nodes: List[nodes.NodeNG], node_statement: nodes.Statement
    ) -> List[nodes.NodeNG]:
        uncertain_nodes: List[nodes.NodeNG] = []
        (
            closest_try_finally_ancestor,
            child_of_closest_try_finally_ancestor,
        ) = utils.get_node_first_ancestor_of_type_and_its_child(
            node_statement, nodes.TryFinally
        )
        if closest_try_finally_ancestor is None:
            return uncertain_nodes
        if (
            child_of_closest_try_finally_ancestor
            not in closest_try_finally_ancestor.finalbody
        ):
            return uncertain_nodes
        for other_node in found_nodes:
            other_node_statement = other_node.statement(future=True)
            (
                other_node_try_finally_ancestor,
                child_of_other_node_try_finally_ancestor,
            ) = utils.get_node_first_ancestor_of_type_and_its_child(
                other_node_statement, nodes.TryFinally
            )
            if other_node_try_finally_ancestor is None:
                continue
            # other_node needs to descend from the try of a try/finally.
            if (
                child_of_other_node_try_finally_ancestor
                not in other_node_try_finally_ancestor.body
            ):
                continue
            # If the two try/finally ancestors are not the same, then
            # node_statement's closest try/finally ancestor needs to be in
            # the final body of other_node's try/finally ancestor, or
            # descend from one of the statements in that final body.
            if (
                other_node_try_finally_ancestor is not closest_try_finally_ancestor
                and not any(
                    other_node_final_statement is closest_try_finally_ancestor
                    or other_node_final_statement.parent_of(
                        closest_try_finally_ancestor
                    )
                    for other_node_final_statement in other_node_try_finally_ancestor.finalbody
                )
            ):
                continue
            # Passed all tests for uncertain execution
            uncertain_nodes.append(other_node)
        return uncertain_nodes


# pylint: disable=too-many-public-methods
class VariablesChecker(BaseChecker):
    """BaseChecker for variables.

    Checks for
    * unused variables / imports
    * undefined variables
    * redefinition of variable from builtins or from an outer scope
    * use of variable before assignment
    * __all__ consistency
    * self/cls assignment
    """

    __implements__ = IAstroidChecker

    name = "variables"
    msgs = MSGS
    priority = -1
    options = (
        (
            "init-import",
            {
                "default": 0,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Tells whether we should check for unused import in "
                "__init__ files.",
            },
        ),
        (
            "dummy-variables-rgx",
            {
                "default": "_+$|(_[a-zA-Z0-9_]*[a-zA-Z0-9]+?$)|dummy|^ignored_|^unused_",
                "type": "regexp",
                "metavar": "<regexp>",
                "help": "A regular expression matching the name of dummy "
                "variables (i.e. expected to not be used).",
            },
        ),
        (
            "additional-builtins",
            {
                "default": (),
                "type": "csv",
                "metavar": "<comma separated list>",
                "help": "List of additional names supposed to be defined in "
                "builtins. Remember that you should avoid defining new builtins "
                "when possible.",
            },
        ),
        (
            "callbacks",
            {
                "default": ("cb_", "_cb"),
                "type": "csv",
                "metavar": "<callbacks>",
                "help": "List of strings which can identify a callback "
                "function by name. A callback name must start or "
                "end with one of those strings.",
            },
        ),
        (
            "redefining-builtins-modules",
            {
                "default": (
                    "six.moves",
                    "past.builtins",
                    "future.builtins",
                    "builtins",
                    "io",
                ),
                "type": "csv",
                "metavar": "<comma separated list>",
                "help": "List of qualified module names which can have objects "
                "that can redefine builtins.",
            },
        ),
        (
            "ignored-argument-names",
            {
                "default": IGNORED_ARGUMENT_NAMES,
                "type": "regexp",
                "metavar": "<regexp>",
                "help": "Argument names that match this expression will be "
                "ignored. Default to name with leading underscore.",
            },
        ),
        (
            "allow-global-unused-variables",
            {
                "default": True,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Tells whether unused global variables should be treated as a violation.",
            },
        ),
        (
            "allowed-redefined-builtins",
            {
                "default": (),
                "type": "csv",
                "metavar": "<comma separated list>",
                "help": "List of names allowed to shadow builtins",
            },
        ),
    )

    def __init__(self, linter=None):
        super().__init__(linter)
        self._to_consume: List[NamesConsumer] = []
        self._checking_mod_attr = None
        self._loop_variables = []
        self._type_annotation_names = []
        self._except_handler_names_queue: List[
            Tuple[nodes.ExceptHandler, nodes.AssignName]
        ] = []
        """This is a queue, last in first out."""
        self._postponed_evaluation_enabled = False

    def open(self) -> None:
        """Called when loading the checker."""
        self._is_undefined_variable_enabled = self.linter.is_message_enabled(
            "undefined-variable"
        )
        self._is_undefined_loop_variable_enabled = self.linter.is_message_enabled(
            "undefined-loop-variable"
        )

    @utils.check_messages("redefined-outer-name")
    def visit_for(self, node: nodes.For) -> None:
        assigned_to = [a.name for a in node.target.nodes_of_class(nodes.AssignName)]

        # Only check variables that are used
        dummy_rgx = self.config.dummy_variables_rgx
        assigned_to = [var for var in assigned_to if not dummy_rgx.match(var)]

        for variable in assigned_to:
            for outer_for, outer_variables in self._loop_variables:
                if variable in outer_variables and not in_for_else_branch(
                    outer_for, node
                ):
                    self.add_message(
                        "redefined-outer-name",
                        args=(variable, outer_for.fromlineno),
                        node=node,
                    )
                    break

        self._loop_variables.append((node, assigned_to))

    @utils.check_messages("redefined-outer-name")
    def leave_for(self, node: nodes.For) -> None:
        self._loop_variables.pop()
        self._store_type_annotation_names(node)

    def visit_module(self, node: nodes.Module) -> None:
        """Visit module : update consumption analysis variable
        checks globals doesn't overrides builtins
        """
        self._to_consume = [NamesConsumer(node, "module")]
        self._postponed_evaluation_enabled = is_postponed_evaluation_enabled(node)

        for name, stmts in node.locals.items():
            if utils.is_builtin(name):
                if self._should_ignore_redefined_builtin(stmts[0]) or name == "__doc__":
                    continue
                self.add_message("redefined-builtin", args=name, node=stmts[0])

    @utils.check_messages(
        "unused-import",
        "unused-wildcard-import",
        "redefined-builtin",
        "undefined-all-variable",
        "invalid-all-object",
        "invalid-all-format",
        "unused-variable",
    )
    def leave_module(self, node: nodes.Module) -> None:
        """Leave module: check globals."""
        assert len(self._to_consume) == 1

        self._check_metaclasses(node)
        not_consumed = self._to_consume.pop().to_consume
        # attempt to check for __all__ if defined
        if "__all__" in node.locals:
            self._check_all(node, not_consumed)

        # check for unused globals
        self._check_globals(not_consumed)

        # don't check unused imports in __init__ files
        if not self.config.init_import and node.package:
            return

        self._check_imports(not_consumed)

    def visit_classdef(self, node: nodes.ClassDef) -> None:
        """Visit class: update consumption analysis variable."""
        self._to_consume.append(NamesConsumer(node, "class"))

    def leave_classdef(self, _: nodes.ClassDef) -> None:
        """Leave class: update consumption analysis variable."""
        # do not check for not used locals here (no sense)
        self._to_consume.pop()

    def visit_lambda(self, node: nodes.Lambda) -> None:
        """Visit lambda: update consumption analysis variable."""
        self._to_consume.append(NamesConsumer(node, "lambda"))

    def leave_lambda(self, _: nodes.Lambda) -> None:
        """Leave lambda: update consumption analysis variable."""
        # do not check for not used locals here
        self._to_consume.pop()

    def visit_generatorexp(self, node: nodes.GeneratorExp) -> None:
        """Visit genexpr: update consumption analysis variable."""
        self._to_consume.append(NamesConsumer(node, "comprehension"))

    def leave_generatorexp(self, _: nodes.GeneratorExp) -> None:
        """Leave genexpr: update consumption analysis variable."""
        # do not check for not used locals here
        self._to_consume.pop()

    def visit_dictcomp(self, node: nodes.DictComp) -> None:
        """Visit dictcomp: update consumption analysis variable."""
        self._to_consume.append(NamesConsumer(node, "comprehension"))

    def leave_dictcomp(self, _: nodes.DictComp) -> None:
        """Leave dictcomp: update consumption analysis variable."""
        # do not check for not used locals here
        self._to_consume.pop()

    def visit_setcomp(self, node: nodes.SetComp) -> None:
        """Visit setcomp: update consumption analysis variable."""
        self._to_consume.append(NamesConsumer(node, "comprehension"))

    def leave_setcomp(self, _: nodes.SetComp) -> None:
        """Leave setcomp: update consumption analysis variable."""
        # do not check for not used locals here
        self._to_consume.pop()

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Visit function: update consumption analysis variable and check locals."""
        self._to_consume.append(NamesConsumer(node, "function"))
        if not (
            self.linter.is_message_enabled("redefined-outer-name")
            or self.linter.is_message_enabled("redefined-builtin")
        ):
            return
        globs = node.root().globals
        for name, stmt in node.items():
            if name in globs and not isinstance(stmt, nodes.Global):
                definition = globs[name][0]
                if (
                    isinstance(definition, nodes.ImportFrom)
                    and definition.modname == FUTURE
                ):
                    # It is a __future__ directive, not a symbol.
                    continue

                # Do not take in account redefined names for the purpose
                # of type checking.:
                if any(
                    isinstance(definition.parent, nodes.If)
                    and definition.parent.test.as_string() in TYPING_TYPE_CHECKS_GUARDS
                    for definition in globs[name]
                ):
                    continue

                line = definition.fromlineno
                if not self._is_name_ignored(stmt, name):
                    self.add_message(
                        "redefined-outer-name", args=(name, line), node=stmt
                    )

            elif (
                utils.is_builtin(name)
                and not self._allowed_redefined_builtin(name)
                and not self._should_ignore_redefined_builtin(stmt)
            ):
                # do not print Redefining builtin for additional builtins
                self.add_message("redefined-builtin", args=name, node=stmt)

    def leave_functiondef(self, node: nodes.FunctionDef) -> None:
        """Leave function: check function's locals are consumed."""
        self._check_metaclasses(node)

        if node.type_comment_returns:
            self._store_type_annotation_node(node.type_comment_returns)
        if node.type_comment_args:
            for argument_annotation in node.type_comment_args:
                self._store_type_annotation_node(argument_annotation)

        not_consumed = self._to_consume.pop().to_consume
        if not (
            self.linter.is_message_enabled("unused-variable")
            or self.linter.is_message_enabled("possibly-unused-variable")
            or self.linter.is_message_enabled("unused-argument")
        ):
            return

        # Don't check arguments of function which are only raising an exception.
        if utils.is_error(node):
            return

        # Don't check arguments of abstract methods or within an interface.
        is_method = node.is_method()
        if is_method and node.is_abstract():
            return

        global_names = _flattened_scope_names(node.nodes_of_class(nodes.Global))
        nonlocal_names = _flattened_scope_names(node.nodes_of_class(nodes.Nonlocal))
        comprehension_target_names: List[str] = []

        for comprehension_scope in node.nodes_of_class(nodes.ComprehensionScope):
            for generator in comprehension_scope.generators:
                self._find_assigned_names_recursive(
                    generator.target, comprehension_target_names
                )

        for name, stmts in not_consumed.items():
            self._check_is_unused(
                name,
                node,
                stmts[0],
                global_names,
                nonlocal_names,
                comprehension_target_names,
            )

    visit_asyncfunctiondef = visit_functiondef
    leave_asyncfunctiondef = leave_functiondef

    @utils.check_messages(
        "global-variable-undefined",
        "global-variable-not-assigned",
        "global-statement",
        "global-at-module-level",
        "redefined-builtin",
    )
    def visit_global(self, node: nodes.Global) -> None:
        """Check names imported exists in the global scope."""
        frame = node.frame(future=True)
        if isinstance(frame, nodes.Module):
            self.add_message("global-at-module-level", node=node)
            return

        module = frame.root()
        default_message = True
        locals_ = node.scope().locals
        for name in node.names:
            try:
                assign_nodes = module.getattr(name)
            except astroid.NotFoundError:
                # unassigned global, skip
                assign_nodes = []

            not_defined_locally_by_import = not any(
                isinstance(local, nodes.Import) for local in locals_.get(name, ())
            )
            if (
                not utils.is_reassigned_after_current(node, name)
                and not utils.is_deleted_after_current(node, name)
                and not_defined_locally_by_import
            ):
                self.add_message("global-variable-not-assigned", args=name, node=node)
                default_message = False
                continue

            for anode in assign_nodes:
                if (
                    isinstance(anode, nodes.AssignName)
                    and anode.name in module.special_attributes
                ):
                    self.add_message("redefined-builtin", args=name, node=node)
                    break
                if anode.frame(future=True) is module:
                    # module level assignment
                    break
                if (
                    isinstance(anode, (nodes.ClassDef, nodes.FunctionDef))
                    and anode.parent is module
                ):
                    # module level function assignment
                    break
            else:
                if not_defined_locally_by_import:
                    # global undefined at the module scope
                    self.add_message("global-variable-undefined", args=name, node=node)
                    default_message = False

        if default_message:
            self.add_message("global-statement", node=node)

    def visit_assignname(self, node: nodes.AssignName) -> None:
        if isinstance(node.assign_type(), nodes.AugAssign):
            self.visit_name(node)

    def visit_delname(self, node: nodes.DelName) -> None:
        self.visit_name(node)

    def visit_name(self, node: nodes.Name) -> None:
        """Don't add the 'utils.check_messages' decorator here!

        It's important that all 'Name' nodes are visited, otherwise the
        'NamesConsumers' won't be correct.
        """
        stmt = node.statement(future=True)
        if stmt.fromlineno is None:
            # name node from an astroid built from live code, skip
            assert not stmt.root().file.endswith(".py")
            return

        self._undefined_and_used_before_checker(node, stmt)
        if self._is_undefined_loop_variable_enabled:
            self._loopvar_name(node)

    @utils.check_messages("redefined-outer-name")
    def visit_excepthandler(self, node: nodes.ExceptHandler) -> None:
        if not node.name or not isinstance(node.name, nodes.AssignName):
            return

        for outer_except, outer_except_assign_name in self._except_handler_names_queue:
            if node.name.name == outer_except_assign_name.name:
                self.add_message(
                    "redefined-outer-name",
                    args=(outer_except_assign_name.name, outer_except.fromlineno),
                    node=node,
                )
                break

        self._except_handler_names_queue.append((node, node.name))

    @utils.check_messages("redefined-outer-name")
    def leave_excepthandler(self, node: nodes.ExceptHandler) -> None:
        if not node.name or not isinstance(node.name, nodes.AssignName):
            return
        self._except_handler_names_queue.pop()

    def _undefined_and_used_before_checker(
        self, node: nodes.Name, stmt: nodes.NodeNG
    ) -> None:
        frame = stmt.scope()
        start_index = len(self._to_consume) - 1

        # iterates through parent scopes, from the inner to the outer
        base_scope_type = self._to_consume[start_index].scope_type

        for i in range(start_index, -1, -1):
            current_consumer = self._to_consume[i]

            # Certain nodes shouldn't be checked as they get checked another time
            if self._should_node_be_skipped(node, current_consumer, i == start_index):
                continue

            action, nodes_to_consume = self._check_consumer(
                node, stmt, frame, current_consumer, base_scope_type
            )
            if nodes_to_consume:
                # Any nodes added to consumed_uncertain by get_next_to_consume()
                # should be added back so that they are marked as used.
                # They will have already had a chance to emit used-before-assignment.
                # We check here instead of before every single return in _check_consumer()
                nodes_to_consume += current_consumer.consumed_uncertain[node.name]
                current_consumer.mark_as_consumed(node.name, nodes_to_consume)
            if action is VariableVisitConsumerAction.CONTINUE:
                continue
            if action is VariableVisitConsumerAction.RETURN:
                return

        # we have not found the name, if it isn't a builtin, that's an
        # undefined name !
        if (
            self._is_undefined_variable_enabled
            and not (
                node.name in nodes.Module.scope_attrs
                or utils.is_builtin(node.name)
                or node.name in self.config.additional_builtins
                or (
                    node.name == "__class__"
                    and isinstance(frame, nodes.FunctionDef)
                    and frame.is_method()
                )
            )
            and not utils.node_ignores_exception(node, NameError)
        ):
            self.add_message("undefined-variable", args=node.name, node=node)

    def _should_node_be_skipped(
        self, node: nodes.Name, consumer: NamesConsumer, is_start_index: bool
    ) -> bool:
        """Tests a consumer and node for various conditions in which the node
        shouldn't be checked for the undefined-variable and used-before-assignment checks.
        """
        if consumer.scope_type == "class":
            # The list of base classes in the class definition is not part
            # of the class body.
            # If the current scope is a class scope but it's not the inner
            # scope, ignore it. This prevents to access this scope instead of
            # the globals one in function members when there are some common
            # names.
            if utils.is_ancestor_name(consumer.node, node) or (
                not is_start_index and self._ignore_class_scope(node)
            ):
                return True

            # Ignore inner class scope for keywords in class definition
            if isinstance(node.parent, nodes.Keyword) and isinstance(
                node.parent.parent, nodes.ClassDef
            ):
                return True

        elif consumer.scope_type == "function" and self._defined_in_function_definition(
            node, consumer.node
        ):
            # If the name node is used as a function default argument's value or as
            # a decorator, then start from the parent frame of the function instead
            # of the function frame - and thus open an inner class scope
            return True

        elif consumer.scope_type == "lambda" and utils.is_default_argument(
            node, consumer.node
        ):
            return True

        return False

    def _find_assigned_names_recursive(
        self,
        target: Union[nodes.AssignName, nodes.BaseContainer],
        target_names: List[str],
    ) -> None:
        """Update `target_names` in place with the names of assignment
        targets, recursively (to account for nested assignments).
        """
        if isinstance(target, nodes.AssignName):
            target_names.append(target.name)
        elif isinstance(target, nodes.BaseContainer):
            for elt in target.elts:
                self._find_assigned_names_recursive(elt, target_names)

    # pylint: disable=too-many-return-statements
    def _check_consumer(
        self,
        node: nodes.Name,
        stmt: nodes.NodeNG,
        frame: nodes.LocalsDictNodeNG,
        current_consumer: NamesConsumer,
        base_scope_type: Any,
    ) -> Tuple[VariableVisitConsumerAction, Optional[List[nodes.NodeNG]]]:
        """Checks a consumer for conditions that should trigger messages."""
        # If the name has already been consumed, only check it's not a loop
        # variable used outside the loop.
        if node.name in current_consumer.consumed:
            # Avoid the case where there are homonyms inside function scope and
            # comprehension current scope (avoid bug #1731)
            if utils.is_func_decorator(current_consumer.node) or not isinstance(
                node, nodes.ComprehensionScope
            ):
                self._check_late_binding_closure(node)
                self._loopvar_name(node)
                return (VariableVisitConsumerAction.RETURN, None)

        found_nodes = current_consumer.get_next_to_consume(node)
        if found_nodes is None:
            return (VariableVisitConsumerAction.CONTINUE, None)
        if not found_nodes:
            if node.name in current_consumer.consumed_uncertain:
                confidence = CONTROL_FLOW
            else:
                confidence = HIGH
            self.add_message(
                "used-before-assignment",
                args=node.name,
                node=node,
                confidence=confidence,
            )
            # Mark for consumption any nodes added to consumed_uncertain by
            # get_next_to_consume() because they might not have executed.
            return (
                VariableVisitConsumerAction.RETURN,
                current_consumer.consumed_uncertain[node.name],
            )

        self._check_late_binding_closure(node)

        defnode = utils.assign_parent(found_nodes[0])
        defstmt = defnode.statement(future=True)
        defframe = defstmt.frame(future=True)

        # The class reuses itself in the class scope.
        is_recursive_klass = (
            frame is defframe
            and defframe.parent_of(node)
            and isinstance(defframe, nodes.ClassDef)
            and node.name == defframe.name
        )

        if (
            is_recursive_klass
            and utils.get_node_first_ancestor_of_type(node, nodes.Lambda)
            and (
                not utils.is_default_argument(node)
                or node.scope().parent.scope() is not defframe
            )
        ):
            # Self-referential class references are fine in lambda's --
            # As long as they are not part of the default argument directly
            # under the scope of the parent self-referring class.
            # Example of valid default argument:
            # class MyName3:
            #     myattr = 1
            #     mylambda3 = lambda: lambda a=MyName3: a
            # Example of invalid default argument:
            # class MyName4:
            #     myattr = 1
            #     mylambda4 = lambda a=MyName4: lambda: a

            # If the above conditional is True,
            # there is no possibility of undefined-variable
            # Also do not consume class name
            # (since consuming blocks subsequent checks)
            # -- quit
            return (VariableVisitConsumerAction.RETURN, None)

        (
            maybe_before_assign,
            annotation_return,
            use_outer_definition,
        ) = self._is_variable_violation(
            node,
            defnode,
            stmt,
            defstmt,
            frame,
            defframe,
            base_scope_type,
            is_recursive_klass,
        )

        if use_outer_definition:
            return (VariableVisitConsumerAction.CONTINUE, None)

        if (
            maybe_before_assign
            and not utils.is_defined_before(node)
            and not astroid.are_exclusive(stmt, defstmt, ("NameError",))
        ):

            # Used and defined in the same place, e.g `x += 1` and `del x`
            defined_by_stmt = defstmt is stmt and isinstance(
                node, (nodes.DelName, nodes.AssignName)
            )
            if (
                is_recursive_klass
                or defined_by_stmt
                or annotation_return
                or isinstance(defstmt, nodes.Delete)
            ):
                if not utils.node_ignores_exception(node, NameError):

                    # Handle postponed evaluation of annotations
                    if not (
                        self._postponed_evaluation_enabled
                        and isinstance(
                            stmt,
                            (
                                nodes.AnnAssign,
                                nodes.FunctionDef,
                                nodes.Arguments,
                            ),
                        )
                        and node.name in node.root().locals
                    ):
                        if defined_by_stmt:
                            return (VariableVisitConsumerAction.CONTINUE, [node])
                        return (VariableVisitConsumerAction.CONTINUE, None)

            elif base_scope_type != "lambda":
                # E0601 may *not* occurs in lambda scope.

                # Handle postponed evaluation of annotations
                if not (
                    self._postponed_evaluation_enabled
                    and isinstance(stmt, (nodes.AnnAssign, nodes.FunctionDef))
                ):
                    self.add_message(
                        "used-before-assignment",
                        args=node.name,
                        node=node,
                        confidence=HIGH,
                    )
                    return (VariableVisitConsumerAction.RETURN, found_nodes)

            elif base_scope_type == "lambda":
                # E0601 can occur in class-level scope in lambdas, as in
                # the following example:
                #   class A:
                #      x = lambda attr: f + attr
                #      f = 42
                # We check lineno because doing the following is fine:
                #   class A:
                #      x = 42
                #      y = lambda attr: x + attr
                if (
                    isinstance(frame, nodes.ClassDef)
                    and node.name in frame.locals
                    and stmt.fromlineno <= defstmt.fromlineno
                ):
                    self.add_message(
                        "used-before-assignment",
                        args=node.name,
                        node=node,
                        confidence=HIGH,
                    )

        elif self._is_only_type_assignment(node, defstmt):
            if node.scope().locals.get(node.name):
                self.add_message(
                    "used-before-assignment", args=node.name, node=node, confidence=HIGH
                )
            else:
                self.add_message(
                    "undefined-variable", args=node.name, node=node, confidence=HIGH
                )
            return (VariableVisitConsumerAction.RETURN, found_nodes)

        elif isinstance(defstmt, nodes.ClassDef):
            return self._is_first_level_self_reference(node, defstmt, found_nodes)

        elif isinstance(defnode, nodes.NamedExpr):
            if isinstance(defnode.parent, nodes.IfExp):
                if self._is_never_evaluated(defnode, defnode.parent):
                    self.add_message(
                        "undefined-variable",
                        args=node.name,
                        node=node,
                        confidence=INFERENCE,
                    )
                    return (VariableVisitConsumerAction.RETURN, found_nodes)

        return (VariableVisitConsumerAction.RETURN, found_nodes)

    @utils.check_messages("no-name-in-module")
    def visit_import(self, node: nodes.Import) -> None:
        """Check modules attribute accesses."""
        if not self._analyse_fallback_blocks and utils.is_from_fallback_block(node):
            # No need to verify this, since ImportError is already
            # handled by the client code.
            return
        if utils.is_node_in_guarded_import_block(node) is True:
            # Don't verify import if part of guarded import block
            # I.e. `sys.version_info` or `typing.TYPE_CHECKING`
            return

        for name, _ in node.names:
            parts = name.split(".")
            try:
                module = next(_infer_name_module(node, parts[0]))
            except astroid.ResolveError:
                continue
            if not isinstance(module, nodes.Module):
                continue
            self._check_module_attrs(node, module, parts[1:])

    @utils.check_messages("no-name-in-module")
    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        """Check modules attribute accesses."""
        if not self._analyse_fallback_blocks and utils.is_from_fallback_block(node):
            # No need to verify this, since ImportError is already
            # handled by the client code.
            return
        if utils.is_node_in_guarded_import_block(node) is True:
            # Don't verify import if part of guarded import block
            # I.e. `sys.version_info` or `typing.TYPE_CHECKING`
            return

        name_parts = node.modname.split(".")
        try:
            module = node.do_import_module(name_parts[0])
        except astroid.AstroidBuildingException:
            return
        module = self._check_module_attrs(node, module, name_parts[1:])
        if not module:
            return
        for name, _ in node.names:
            if name == "*":
                continue
            self._check_module_attrs(node, module, name.split("."))

    @utils.check_messages(
        "unbalanced-tuple-unpacking", "unpacking-non-sequence", "self-cls-assignment"
    )
    def visit_assign(self, node: nodes.Assign) -> None:
        """Check unbalanced tuple unpacking for assignments and unpacking
        non-sequences as well as in case self/cls get assigned.
        """
        self._check_self_cls_assign(node)
        if not isinstance(node.targets[0], (nodes.Tuple, nodes.List)):
            return

        targets = node.targets[0].itered()
        try:
            inferred = utils.safe_infer(node.value)
            if inferred is not None:
                self._check_unpacking(inferred, node, targets)
        except astroid.InferenceError:
            return

    # listcomp have now also their scope
    def visit_listcomp(self, node: nodes.ListComp) -> None:
        """Visit dictcomp: update consumption analysis variable."""
        self._to_consume.append(NamesConsumer(node, "comprehension"))

    def leave_listcomp(self, _: nodes.ListComp) -> None:
        """Leave dictcomp: update consumption analysis variable."""
        # do not check for not used locals here
        self._to_consume.pop()

    def leave_assign(self, node: nodes.Assign) -> None:
        self._store_type_annotation_names(node)

    def leave_with(self, node: nodes.With) -> None:
        self._store_type_annotation_names(node)

    def visit_arguments(self, node: nodes.Arguments) -> None:
        for annotation in node.type_comment_args:
            self._store_type_annotation_node(annotation)

    # Relying on other checker's options, which might not have been initialized yet.
    @cached_property
    def _analyse_fallback_blocks(self):
        return get_global_option(self, "analyse-fallback-blocks", default=False)

    @cached_property
    def _ignored_modules(self):
        return get_global_option(self, "ignored-modules", default=[])

    @cached_property
    def _allow_global_unused_variables(self):
        return get_global_option(self, "allow-global-unused-variables", default=True)

    @staticmethod
    def _defined_in_function_definition(node, frame):
        in_annotation_or_default_or_decorator = False
        if (
            isinstance(frame, nodes.FunctionDef)
            and node.statement(future=True) is frame
        ):
            in_annotation_or_default_or_decorator = (
                (
                    node in frame.args.annotations
                    or node in frame.args.posonlyargs_annotations
                    or node in frame.args.kwonlyargs_annotations
                    or node is frame.args.varargannotation
                    or node is frame.args.kwargannotation
                )
                or frame.args.parent_of(node)
                or (frame.decorators and frame.decorators.parent_of(node))
                or (
                    frame.returns
                    and (node is frame.returns or frame.returns.parent_of(node))
                )
            )
        return in_annotation_or_default_or_decorator

    @staticmethod
    def _in_lambda_or_comprehension_body(
        node: nodes.NodeNG, frame: nodes.NodeNG
    ) -> bool:
        """Return True if node within a lambda/comprehension body (or similar) and thus should not have access to class attributes in frame."""
        child = node
        parent = node.parent
        while parent is not None:
            if parent is frame:
                return False
            if isinstance(parent, nodes.Lambda) and child is not parent.args:
                # Body of lambda should not have access to class attributes.
                return True
            if isinstance(parent, nodes.Comprehension) and child is not parent.iter:
                # Only iter of list/set/dict/generator comprehension should have access.
                return True
            if isinstance(parent, nodes.ComprehensionScope) and not (
                parent.generators and child is parent.generators[0]
            ):
                # Body of list/set/dict/generator comprehension should not have access to class attributes.
                # Furthermore, only the first generator (if multiple) in comprehension should have access.
                return True
            child = parent
            parent = parent.parent
        return False

    @staticmethod
    def _is_variable_violation(
        node: nodes.Name,
        defnode,
        stmt: nodes.Statement,
        defstmt: nodes.Statement,
        frame,  # scope of statement of node
        defframe,
        base_scope_type,
        is_recursive_klass,
    ) -> Tuple[bool, bool, bool]:
        # pylint: disable=too-many-nested-blocks
        maybe_before_assign = True
        annotation_return = False
        use_outer_definition = False
        if frame is not defframe:
            maybe_before_assign = _detect_global_scope(node, frame, defframe)
        elif defframe.parent is None:
            # we are at the module level, check the name is not
            # defined in builtins
            if (
                node.name in defframe.scope_attrs
                or astroid.builtin_lookup(node.name)[1]
            ):
                maybe_before_assign = False
        else:
            # we are in a local scope, check the name is not
            # defined in global or builtin scope
            # skip this lookup if name is assigned later in function scope/lambda
            # Note: the node.frame() is not the same as the `frame` argument which is
            # equivalent to frame.statement().scope()
            forbid_lookup = (
                isinstance(frame, nodes.FunctionDef)
                or isinstance(node.frame(future=True), nodes.Lambda)
            ) and _assigned_locally(node)
            if not forbid_lookup and defframe.root().lookup(node.name)[1]:
                maybe_before_assign = False
                use_outer_definition = stmt == defstmt and not isinstance(
                    defnode, nodes.Comprehension
                )
            # check if we have a nonlocal
            elif node.name in defframe.locals:
                maybe_before_assign = not any(
                    isinstance(child, nodes.Nonlocal) and node.name in child.names
                    for child in defframe.get_children()
                )

        if (
            base_scope_type == "lambda"
            and isinstance(frame, nodes.ClassDef)
            and node.name in frame.locals
        ):

            # This rule verifies that if the definition node of the
            # checked name is an Arguments node and if the name
            # is used a default value in the arguments defaults
            # and the actual definition of the variable label
            # is happening before the Arguments definition.
            #
            # bar = None
            # foo = lambda bar=bar: bar
            #
            # In this case, maybe_before_assign should be False, otherwise
            # it should be True.
            maybe_before_assign = not (
                isinstance(defnode, nodes.Arguments)
                and node in defnode.defaults
                and frame.locals[node.name][0].fromlineno < defstmt.fromlineno
            )
        elif isinstance(defframe, nodes.ClassDef) and isinstance(
            frame, nodes.FunctionDef
        ):
            # Special rule for function return annotations,
            # using a name defined earlier in the class containing the function.
            if node is frame.returns and defframe.parent_of(frame.returns):
                annotation_return = True
                if (
                    frame.returns.name in defframe.locals
                    and defframe.locals[node.name][0].lineno < frame.lineno
                ):
                    # Detect class assignments with a name defined earlier in the
                    # class. In this case, no warning should be raised.
                    maybe_before_assign = False
                else:
                    maybe_before_assign = True
            if isinstance(node.parent, nodes.Arguments):
                maybe_before_assign = stmt.fromlineno <= defstmt.fromlineno
        elif is_recursive_klass:
            maybe_before_assign = True
        else:
            maybe_before_assign = (
                maybe_before_assign and stmt.fromlineno <= defstmt.fromlineno
            )
            if maybe_before_assign and stmt.fromlineno == defstmt.fromlineno:
                if (
                    isinstance(defframe, nodes.FunctionDef)
                    and frame is defframe
                    and defframe.parent_of(node)
                    and stmt is not defstmt
                ):
                    # Single statement function, with the statement on the
                    # same line as the function definition
                    maybe_before_assign = False
                elif (
                    isinstance(
                        defstmt,
                        (
                            nodes.Assign,
                            nodes.AnnAssign,
                            nodes.AugAssign,
                            nodes.Expr,
                            nodes.Return,
                        ),
                    )
                    and VariablesChecker._maybe_used_and_assigned_at_once(defstmt)
                    and frame is defframe
                    and defframe.parent_of(node)
                    and stmt is defstmt
                ):
                    # Single statement if, with assignment expression on same
                    # line as assignment
                    # x = b if (b := True) else False
                    maybe_before_assign = False
                elif (
                    isinstance(  # pylint: disable=too-many-boolean-expressions
                        defnode, nodes.NamedExpr
                    )
                    and frame is defframe
                    and defframe.parent_of(stmt)
                    and stmt is defstmt
                    and (
                        (
                            defnode.lineno == node.lineno
                            and defnode.col_offset < node.col_offset
                        )
                        or (defnode.lineno < node.lineno)
                        or (
                            # Issue in the `ast` module until py39
                            # Nodes in a multiline string have the same lineno
                            # Could be false-positive without check
                            not PY39_PLUS
                            and defnode.lineno == node.lineno
                            and isinstance(
                                defstmt,
                                (
                                    nodes.Assign,
                                    nodes.AnnAssign,
                                    nodes.AugAssign,
                                    nodes.Return,
                                ),
                            )
                            and isinstance(defstmt.value, nodes.JoinedStr)
                        )
                    )
                ):
                    # Expressions, with assignment expressions
                    # Use only after assignment
                    # b = (c := 2) and c
                    maybe_before_assign = False

            # Look for type checking definitions inside a type checking guard.
            if isinstance(defstmt, (nodes.Import, nodes.ImportFrom)):
                defstmt_parent = defstmt.parent

                if (
                    isinstance(defstmt_parent, nodes.If)
                    and defstmt_parent.test.as_string() in TYPING_TYPE_CHECKS_GUARDS
                ):
                    # Exempt those definitions that are used inside the type checking
                    # guard or that are defined in both type checking guard branches.
                    used_in_branch = defstmt_parent.parent_of(node)
                    defined_in_or_else = False

                    for definition in defstmt_parent.orelse:
                        if isinstance(definition, nodes.Assign):
                            defined_in_or_else = any(
                                target.name == node.name
                                for target in definition.targets
                                if isinstance(target, nodes.AssignName)
                            )
                            if defined_in_or_else:
                                break

                    if not used_in_branch and not defined_in_or_else:
                        maybe_before_assign = True

        return maybe_before_assign, annotation_return, use_outer_definition

    @staticmethod
    def _maybe_used_and_assigned_at_once(defstmt: nodes.Statement) -> bool:
        """Check if `defstmt` has the potential to use and assign a name in the
        same statement.
        """
        if isinstance(defstmt.value, nodes.BaseContainer) and defstmt.value.elts:
            # The assignment must happen as part of the first element
            # e.g. "assert (x:= True), x"
            # NOT "assert x, (x:= True)"
            value = defstmt.value.elts[0]
        else:
            value = defstmt.value
        if isinstance(value, nodes.IfExp):
            return True
        if isinstance(value, nodes.Lambda) and isinstance(value.body, nodes.IfExp):
            return True
        return isinstance(value, nodes.Call) and (
            any(isinstance(kwarg.value, nodes.IfExp) for kwarg in value.keywords)
            or any(isinstance(arg, nodes.IfExp) for arg in value.args)
        )

    def _is_only_type_assignment(
        self, node: nodes.Name, defstmt: nodes.Statement
    ) -> bool:
        """Check if variable only gets assigned a type and never a value."""
        if not isinstance(defstmt, nodes.AnnAssign) or defstmt.value:
            return False

        if node.name in self.config.additional_builtins or utils.is_builtin(node.name):
            return False

        defstmt_frame = defstmt.frame(future=True)
        node_frame = node.frame(future=True)

        parent = node
        while parent is not defstmt_frame.parent:
            parent_scope = parent.scope()

            # Find out if any nonlocals receive values in nested functions
            for inner_func in parent_scope.nodes_of_class(nodes.FunctionDef):
                if inner_func is parent_scope:
                    continue
                if any(
                    node.name in nl.names
                    for nl in inner_func.nodes_of_class(nodes.Nonlocal)
                ) and any(
                    node.name == an.name
                    for an in inner_func.nodes_of_class(nodes.AssignName)
                ):
                    return False

            local_refs = parent_scope.locals.get(node.name, [])
            for ref_node in local_refs:
                # If local ref is in the same frame as our node, but on a later lineno
                # we don't actually care about this local ref.
                # Local refs are ordered, so we break.
                #     print(var)
                #     var = 1  # <- irrelevant
                if defstmt_frame == node_frame and ref_node.lineno > node.lineno:
                    break

                # If the parent of the local reference is anything but an AnnAssign
                # Or if the AnnAssign adds a value the variable will now have a value
                #     var = 1  # OR
                #     var: int = 1
                if (
                    not isinstance(ref_node.parent, nodes.AnnAssign)
                    or ref_node.parent.value
                ):
                    return False
            parent = parent_scope.parent
        return True

    @staticmethod
    def _is_first_level_self_reference(
        node: nodes.Name, defstmt: nodes.ClassDef, found_nodes: List[nodes.NodeNG]
    ) -> Tuple[VariableVisitConsumerAction, Optional[List[nodes.NodeNG]]]:
        """Check if a first level method's annotation or default values
        refers to its own class, and return a consumer action
        """
        if node.frame(future=True).parent == defstmt and node.statement(
            future=True
        ) == node.frame(future=True):
            # Check if used as type annotation
            # Break if postponed evaluation is enabled
            if utils.is_node_in_type_annotation_context(node):
                if not utils.is_postponed_evaluation_enabled(node):
                    return (VariableVisitConsumerAction.CONTINUE, None)
                return (VariableVisitConsumerAction.RETURN, None)
            # Check if used as default value by calling the class
            if isinstance(node.parent, nodes.Call) and isinstance(
                node.parent.parent, nodes.Arguments
            ):
                return (VariableVisitConsumerAction.CONTINUE, None)
        return (VariableVisitConsumerAction.RETURN, found_nodes)

    @staticmethod
    def _is_never_evaluated(
        defnode: nodes.NamedExpr, defnode_parent: nodes.IfExp
    ) -> bool:
        """Check if a NamedExpr is inside a side of if ... else that never
        gets evaluated
        """
        inferred_test = utils.safe_infer(defnode_parent.test)
        if isinstance(inferred_test, nodes.Const):
            if inferred_test.value is True and defnode == defnode_parent.orelse:
                return True
            if inferred_test.value is False and defnode == defnode_parent.body:
                return True
        return False

    def _ignore_class_scope(self, node):
        """Return True if the node is in a local class scope, as an assignment.

        :param node: Node considered
        :type node: astroid.Node
        :return: True if the node is in a local class scope, as an assignment. False otherwise.
        :rtype: bool
        """
        # Detect if we are in a local class scope, as an assignment.
        # For example, the following is fair game.
        #
        # class A:
        #    b = 1
        #    c = lambda b=b: b * b
        #
        # class B:
        #    tp = 1
        #    def func(self, arg: tp):
        #        ...
        # class C:
        #    tp = 2
        #    def func(self, arg=tp):
        #        ...
        # class C:
        #    class Tp:
        #        pass
        #    class D(Tp):
        #        ...

        name = node.name
        frame = node.statement(future=True).scope()
        in_annotation_or_default_or_decorator = self._defined_in_function_definition(
            node, frame
        )
        in_ancestor_list = utils.is_ancestor_name(frame, node)
        if in_annotation_or_default_or_decorator or in_ancestor_list:
            frame_locals = frame.parent.scope().locals
        else:
            frame_locals = frame.locals
        return not (
            (isinstance(frame, nodes.ClassDef) or in_annotation_or_default_or_decorator)
            and not self._in_lambda_or_comprehension_body(node, frame)
            and name in frame_locals
        )

    def _loopvar_name(self, node: astroid.Name) -> None:
        # filter variables according to node's scope
        astmts = [s for s in node.lookup(node.name)[1] if hasattr(s, "assign_type")]
        # If this variable usage exists inside a function definition
        # that exists in the same loop,
        # the usage is safe because the function will not be defined either if
        # the variable is not defined.
        scope = node.scope()
        # FunctionDef subclasses Lambda due to a curious ontology. Check both.
        # See https://github.com/PyCQA/astroid/issues/291
        # pylint: disable-next=fixme
        # TODO: Revisit when astroid 3.0 includes the change
        if isinstance(scope, nodes.Lambda) and any(
            asmt.scope().parent_of(scope) for asmt in astmts
        ):
            return
        # Filter variables according to their respective scope. Test parent
        # and statement to avoid #74747. This is not a total fix, which would
        # introduce a mechanism similar to special attribute lookup in
        # modules. Also, in order to get correct inference in this case, the
        # scope lookup rules would need to be changed to return the initial
        # assignment (which does not exist in code per se) as well as any later
        # modifications.
        # pylint: disable-next=too-many-boolean-expressions
        if (
            not astmts
            or (
                astmts[0].parent == astmts[0].root()
                and astmts[0].parent.parent_of(node)
            )
            or (
                astmts[0].is_statement
                or not isinstance(astmts[0].parent, nodes.Module)
                and astmts[0].statement(future=True).parent_of(node)
            )
        ):
            _astmts = []
        else:
            _astmts = astmts[:1]
        for i, stmt in enumerate(astmts[1:]):
            if astmts[i].statement(future=True).parent_of(
                stmt
            ) and not in_for_else_branch(astmts[i].statement(future=True), stmt):
                continue
            _astmts.append(stmt)
        astmts = _astmts
        if len(astmts) != 1:
            return

        assign = astmts[0].assign_type()
        if not (
            isinstance(assign, (nodes.For, nodes.Comprehension, nodes.GeneratorExp))
            and assign.statement(future=True) is not node.statement(future=True)
        ):
            return

        if not isinstance(assign, nodes.For):
            self.add_message("undefined-loop-variable", args=node.name, node=node)
            return
        if any(
            isinstance(else_stmt, (nodes.Return, nodes.Raise))
            for else_stmt in assign.orelse
        ):
            return

        # For functions we can do more by inferring the length of the itered object
        try:
            inferred = next(assign.iter.infer())
            # Prefer the target of enumerate() rather than the enumerate object itself
            if (
                isinstance(inferred, astroid.Instance)
                and inferred.qname() == "builtins.enumerate"
                and assign.iter.args
            ):
                inferred = next(assign.iter.args[0].infer())
        except astroid.InferenceError:
            self.add_message("undefined-loop-variable", args=node.name, node=node)
        else:
            if (
                isinstance(inferred, astroid.Instance)
                and inferred.qname() == BUILTIN_RANGE
            ):
                # Consider range() objects safe, even if they might not yield any results.
                return

            # Consider sequences.
            sequences = (
                nodes.List,
                nodes.Tuple,
                nodes.Dict,
                nodes.Set,
                astroid.objects.FrozenSet,
            )
            if not isinstance(inferred, sequences):
                self.add_message("undefined-loop-variable", args=node.name, node=node)
                return

            elements = getattr(inferred, "elts", getattr(inferred, "items", []))
            if not elements:
                self.add_message("undefined-loop-variable", args=node.name, node=node)

    def _check_is_unused(
        self,
        name,
        node,
        stmt,
        global_names,
        nonlocal_names: Iterable[str],
        comprehension_target_names: List[str],
    ) -> None:
        # Ignore some special names specified by user configuration.
        if self._is_name_ignored(stmt, name):
            return
        # Ignore names that were added dynamically to the Function scope
        if (
            isinstance(node, nodes.FunctionDef)
            and name == "__class__"
            and len(node.locals["__class__"]) == 1
            and isinstance(node.locals["__class__"][0], nodes.ClassDef)
        ):
            return

        # Ignore names imported by the global statement.
        if isinstance(stmt, (nodes.Global, nodes.Import, nodes.ImportFrom)):
            # Detect imports, assigned to global statements.
            if global_names and _import_name_is_global(stmt, global_names):
                return

        # Ignore names in comprehension targets
        if name in comprehension_target_names:
            return

        argnames = node.argnames()
        # Care about functions with unknown argument (builtins)
        if name in argnames:
            self._check_unused_arguments(name, node, stmt, argnames, nonlocal_names)
        else:
            if stmt.parent and isinstance(
                stmt.parent, (nodes.Assign, nodes.AnnAssign, nodes.Tuple)
            ):
                if name in nonlocal_names:
                    return

            qname = asname = None
            if isinstance(stmt, (nodes.Import, nodes.ImportFrom)):
                # Need the complete name, which we don't have in .locals.
                if len(stmt.names) > 1:
                    import_names = next(
                        (names for names in stmt.names if name in names), None
                    )
                else:
                    import_names = stmt.names[0]
                if import_names:
                    qname, asname = import_names
                    name = asname or qname

            if _has_locals_call_after_node(stmt, node.scope()):
                message_name = "possibly-unused-variable"
            else:
                if isinstance(stmt, nodes.Import):
                    if asname is not None:
                        msg = f"{qname} imported as {asname}"
                    else:
                        msg = f"import {name}"
                    self.add_message("unused-import", args=msg, node=stmt)
                    return
                if isinstance(stmt, nodes.ImportFrom):
                    if asname is not None:
                        msg = f"{qname} imported from {stmt.modname} as {asname}"
                    else:
                        msg = f"{name} imported from {stmt.modname}"
                    self.add_message("unused-import", args=msg, node=stmt)
                    return
                message_name = "unused-variable"

            if isinstance(stmt, nodes.FunctionDef) and stmt.decorators:
                return

            # Don't check function stubs created only for type information
            if utils.is_overload_stub(node):
                return

            # Special case for exception variable
            if isinstance(stmt.parent, nodes.ExceptHandler) and any(
                n.name == name for n in stmt.parent.nodes_of_class(nodes.Name)
            ):
                return

            self.add_message(message_name, args=name, node=stmt)

    def _is_name_ignored(self, stmt, name):
        authorized_rgx = self.config.dummy_variables_rgx
        if (
            isinstance(stmt, nodes.AssignName)
            and isinstance(stmt.parent, nodes.Arguments)
            or isinstance(stmt, nodes.Arguments)
        ):
            regex = self.config.ignored_argument_names
        else:
            regex = authorized_rgx
        return regex and regex.match(name)

    def _check_unused_arguments(
        self, name, node, stmt, argnames, nonlocal_names: Iterable[str]
    ):
        is_method = node.is_method()
        klass = node.parent.frame(future=True)
        if is_method and isinstance(klass, nodes.ClassDef):
            confidence = (
                INFERENCE if utils.has_known_bases(klass) else INFERENCE_FAILURE
            )
        else:
            confidence = HIGH

        if is_method:
            # Don't warn for the first argument of a (non static) method
            if node.type != "staticmethod" and name == argnames[0]:
                return
            # Don't warn for argument of an overridden method
            overridden = overridden_method(klass, node.name)
            if overridden is not None and name in overridden.argnames():
                return
            if node.name in utils.PYMETHODS and node.name not in (
                "__init__",
                "__new__",
            ):
                return
        # Don't check callback arguments
        if any(
            node.name.startswith(cb) or node.name.endswith(cb)
            for cb in self.config.callbacks
        ):
            return
        # Don't check arguments of singledispatch.register function.
        if utils.is_registered_in_singledispatch_function(node):
            return

        # Don't check function stubs created only for type information
        if utils.is_overload_stub(node):
            return

        # Don't check protocol classes
        if utils.is_protocol_class(klass):
            return

        if name in nonlocal_names:
            return

        self.add_message("unused-argument", args=name, node=stmt, confidence=confidence)

    def _check_late_binding_closure(self, node: nodes.Name) -> None:
        """Check whether node is a cell var that is assigned within a containing loop.

        Special cases where we don't care about the error:
        1. When the node's function is immediately called, e.g. (lambda: i)()
        2. When the node's function is returned from within the loop, e.g. return lambda: i
        """
        if not self.linter.is_message_enabled("cell-var-from-loop"):
            return

        node_scope = node.frame(future=True)

        # If node appears in a default argument expression,
        # look at the next enclosing frame instead
        if utils.is_default_argument(node, node_scope):
            node_scope = node_scope.parent.frame(future=True)

        # Check if node is a cell var
        if (
            not isinstance(node_scope, (nodes.Lambda, nodes.FunctionDef))
            or node.name in node_scope.locals
        ):
            return

        assign_scope, stmts = node.lookup(node.name)
        if not stmts or not assign_scope.parent_of(node_scope):
            return

        if utils.is_comprehension(assign_scope):
            self.add_message("cell-var-from-loop", node=node, args=node.name)
        else:
            # Look for an enclosing For loop.
            # Currently, we only consider the first assignment
            assignment_node = stmts[0]

            maybe_for = assignment_node
            while maybe_for and not isinstance(maybe_for, nodes.For):
                if maybe_for is assign_scope:
                    break
                maybe_for = maybe_for.parent
            else:
                if (
                    maybe_for
                    and maybe_for.parent_of(node_scope)
                    and not utils.is_being_called(node_scope)
                    and node_scope.parent
                    and not isinstance(node_scope.statement(future=True), nodes.Return)
                ):
                    self.add_message("cell-var-from-loop", node=node, args=node.name)

    def _should_ignore_redefined_builtin(self, stmt):
        if not isinstance(stmt, nodes.ImportFrom):
            return False
        return stmt.modname in self.config.redefining_builtins_modules

    def _allowed_redefined_builtin(self, name):
        return name in self.config.allowed_redefined_builtins

    @staticmethod
    def _comprehension_between_frame_and_node(node: nodes.Name) -> bool:
        """Return True if a ComprehensionScope intervenes between `node` and its frame."""
        closest_comprehension_scope = utils.get_node_first_ancestor_of_type(
            node, nodes.ComprehensionScope
        )
        return closest_comprehension_scope is not None and node.frame(
            future=True
        ).parent_of(closest_comprehension_scope)

    def _store_type_annotation_node(self, type_annotation):
        """Given a type annotation, store all the name nodes it refers to."""
        if isinstance(type_annotation, nodes.Name):
            self._type_annotation_names.append(type_annotation.name)
            return

        if isinstance(type_annotation, nodes.Attribute):
            self._store_type_annotation_node(type_annotation.expr)
            return

        if not isinstance(type_annotation, nodes.Subscript):
            return

        if (
            isinstance(type_annotation.value, nodes.Attribute)
            and isinstance(type_annotation.value.expr, nodes.Name)
            and type_annotation.value.expr.name == TYPING_MODULE
        ):
            self._type_annotation_names.append(TYPING_MODULE)
            return

        self._type_annotation_names.extend(
            annotation.name for annotation in type_annotation.nodes_of_class(nodes.Name)
        )

    def _store_type_annotation_names(self, node):
        type_annotation = node.type_annotation
        if not type_annotation:
            return
        self._store_type_annotation_node(node.type_annotation)

    def _check_self_cls_assign(self, node: nodes.Assign) -> None:
        """Check that self/cls don't get assigned."""
        assign_names: Set[Optional[str]] = set()
        for target in node.targets:
            if isinstance(target, nodes.AssignName):
                assign_names.add(target.name)
            elif isinstance(target, nodes.Tuple):
                assign_names.update(
                    elt.name for elt in target.elts if isinstance(elt, nodes.AssignName)
                )
        scope = node.scope()
        nonlocals_with_same_name = any(
            child for child in scope.body if isinstance(child, nodes.Nonlocal)
        )
        if nonlocals_with_same_name:
            scope = node.scope().parent.scope()

        if not (
            isinstance(scope, nodes.FunctionDef)
            and scope.is_method()
            and "builtins.staticmethod" not in scope.decoratornames()
        ):
            return
        argument_names = scope.argnames()
        if not argument_names:
            return
        self_cls_name = argument_names[0]
        if self_cls_name in assign_names:
            self.add_message("self-cls-assignment", node=node, args=(self_cls_name,))

    def _check_unpacking(self, inferred, node, targets):
        """Check for unbalanced tuple unpacking
        and unpacking non sequences.
        """
        if utils.is_inside_abstract_class(node):
            return
        if utils.is_comprehension(node):
            return
        if inferred is astroid.Uninferable:
            return
        if (
            isinstance(inferred.parent, nodes.Arguments)
            and isinstance(node.value, nodes.Name)
            and node.value.name == inferred.parent.vararg
        ):
            # Variable-length argument, we can't determine the length.
            return

        # Attempt to check unpacking is properly balanced
        values = self._nodes_to_unpack(inferred)
        if values is not None:
            if len(targets) != len(values):
                # Check if we have starred nodes.
                if any(isinstance(target, nodes.Starred) for target in targets):
                    return
                self.add_message(
                    "unbalanced-tuple-unpacking",
                    node=node,
                    args=(
                        _get_unpacking_extra_info(node, inferred),
                        len(targets),
                        len(values),
                    ),
                )
        # attempt to check unpacking may be possible (ie RHS is iterable)
        elif not utils.is_iterable(inferred):
            self.add_message(
                "unpacking-non-sequence",
                node=node,
                args=(_get_unpacking_extra_info(node, inferred),),
            )

    @staticmethod
    def _nodes_to_unpack(node: nodes.NodeNG) -> Optional[List[nodes.NodeNG]]:
        """Return the list of values of the `Assign` node."""
        if isinstance(node, (nodes.Tuple, nodes.List)):
            return node.itered()
        if isinstance(node, astroid.Instance) and any(
            ancestor.qname() == "typing.NamedTuple" for ancestor in node.ancestors()
        ):
            return [i for i in node.values() if isinstance(i, nodes.AssignName)]
        return None

    def _check_module_attrs(self, node, module, module_names):
        """Check that module_names (list of string) are accessible through the
        given module, if the latest access name corresponds to a module, return it
        """
        while module_names:
            name = module_names.pop(0)
            if name == "__dict__":
                module = None
                break
            try:
                module = next(module.getattr(name)[0].infer())
                if module is astroid.Uninferable:
                    return None
            except astroid.NotFoundError:
                if module.name in self._ignored_modules:
                    return None
                self.add_message(
                    "no-name-in-module", args=(name, module.name), node=node
                )
                return None
            except astroid.InferenceError:
                return None
        if module_names:
            modname = module.name if module else "__dict__"
            self.add_message(
                "no-name-in-module", node=node, args=(".".join(module_names), modname)
            )
            return None
        if isinstance(module, nodes.Module):
            return module
        return None

    def _check_all(self, node: nodes.Module, not_consumed):
        assigned = next(node.igetattr("__all__"))
        if assigned is astroid.Uninferable:
            return
        if not assigned.pytype() in {"builtins.list", "builtins.tuple"}:
            line, col = assigned.tolineno, assigned.col_offset
            self.add_message("invalid-all-format", line=line, col_offset=col, node=node)
            return
        for elt in getattr(assigned, "elts", ()):
            try:
                elt_name = next(elt.infer())
            except astroid.InferenceError:
                continue
            if elt_name is astroid.Uninferable:
                continue
            if not elt_name.parent:
                continue

            if not isinstance(elt_name, nodes.Const) or not isinstance(
                elt_name.value, str
            ):
                self.add_message("invalid-all-object", args=elt.as_string(), node=elt)
                continue

            elt_name = elt_name.value
            # If elt is in not_consumed, remove it from not_consumed
            if elt_name in not_consumed:
                del not_consumed[elt_name]
                continue

            if elt_name not in node.locals:
                if not node.package:
                    self.add_message(
                        "undefined-all-variable", args=(elt_name,), node=elt
                    )
                else:
                    basename = os.path.splitext(node.file)[0]
                    if os.path.basename(basename) == "__init__":
                        name = node.name + "." + elt_name
                        try:
                            astroid.modutils.file_from_modpath(name.split("."))
                        except ImportError:
                            self.add_message(
                                "undefined-all-variable", args=(elt_name,), node=elt
                            )
                        except SyntaxError:
                            # don't yield a syntax-error warning,
                            # because it will be later yielded
                            # when the file will be checked
                            pass

    def _check_globals(self, not_consumed):
        if self._allow_global_unused_variables:
            return
        for name, node_lst in not_consumed.items():
            for node in node_lst:
                self.add_message("unused-variable", args=(name,), node=node)

    def _check_imports(self, not_consumed):
        local_names = _fix_dot_imports(not_consumed)
        checked = set()
        unused_wildcard_imports: DefaultDict[
            Tuple[str, nodes.ImportFrom], List[str]
        ] = collections.defaultdict(list)
        for name, stmt in local_names:
            for imports in stmt.names:
                real_name = imported_name = imports[0]
                if imported_name == "*":
                    real_name = name
                as_name = imports[1]
                if real_name in checked:
                    continue
                if name not in (real_name, as_name):
                    continue
                checked.add(real_name)

                is_type_annotation_import = (
                    imported_name in self._type_annotation_names
                    or as_name in self._type_annotation_names
                )
                if isinstance(stmt, nodes.Import) or (
                    isinstance(stmt, nodes.ImportFrom) and not stmt.modname
                ):
                    if isinstance(stmt, nodes.ImportFrom) and SPECIAL_OBJ.search(
                        imported_name
                    ):
                        # Filter special objects (__doc__, __all__) etc.,
                        # because they can be imported for exporting.
                        continue

                    if is_type_annotation_import:
                        # Most likely a typing import if it wasn't used so far.
                        continue

                    if as_name == "_":
                        continue
                    if as_name is None:
                        msg = f"import {imported_name}"
                    else:
                        msg = f"{imported_name} imported as {as_name}"
                    if not in_type_checking_block(stmt):
                        self.add_message("unused-import", args=msg, node=stmt)
                elif isinstance(stmt, nodes.ImportFrom) and stmt.modname != FUTURE:
                    if SPECIAL_OBJ.search(imported_name):
                        # Filter special objects (__doc__, __all__) etc.,
                        # because they can be imported for exporting.
                        continue

                    if _is_from_future_import(stmt, name):
                        # Check if the name is in fact loaded from a
                        # __future__ import in another module.
                        continue

                    if is_type_annotation_import:
                        # Most likely a typing import if it wasn't used so far.
                        continue

                    if imported_name == "*":
                        unused_wildcard_imports[(stmt.modname, stmt)].append(name)
                    else:
                        if as_name is None:
                            msg = f"{imported_name} imported from {stmt.modname}"
                        else:
                            msg = f"{imported_name} imported from {stmt.modname} as {as_name}"
                        if not in_type_checking_block(stmt):
                            self.add_message("unused-import", args=msg, node=stmt)

        # Construct string for unused-wildcard-import message
        for module, unused_list in unused_wildcard_imports.items():
            if len(unused_list) == 1:
                arg_string = unused_list[0]
            else:
                arg_string = (
                    f"{', '.join(i for i in unused_list[:-1])} and {unused_list[-1]}"
                )
            self.add_message(
                "unused-wildcard-import", args=(arg_string, module[0]), node=module[1]
            )
        del self._to_consume

    def _check_metaclasses(self, node):
        """Update consumption analysis for metaclasses."""
        consumed = []  # [(scope_locals, consumed_key)]

        for child_node in node.get_children():
            if isinstance(child_node, nodes.ClassDef):
                consumed.extend(self._check_classdef_metaclasses(child_node, node))

        # Pop the consumed items, in order to avoid having
        # unused-import and unused-variable false positives
        for scope_locals, name in consumed:
            scope_locals.pop(name, None)

    def _check_classdef_metaclasses(self, klass, parent_node):
        if not klass._metaclass:
            # Skip if this class doesn't use explicitly a metaclass, but inherits it from ancestors
            return []

        consumed = []  # [(scope_locals, consumed_key)]
        metaclass = klass.metaclass()
        name = None
        if isinstance(klass._metaclass, nodes.Name):
            name = klass._metaclass.name
        elif isinstance(klass._metaclass, nodes.Attribute) and klass._metaclass.expr:
            attr = klass._metaclass.expr
            while not isinstance(attr, nodes.Name):
                attr = attr.expr
            name = attr.name
        elif isinstance(klass._metaclass, nodes.Call) and isinstance(
            klass._metaclass.func, nodes.Name
        ):
            name = klass._metaclass.func.name
        elif metaclass:
            name = metaclass.root().name

        found = False
        name = METACLASS_NAME_TRANSFORMS.get(name, name)
        if name:
            # check enclosing scopes starting from most local
            for scope_locals, _, _, _ in self._to_consume[::-1]:
                found_nodes = scope_locals.get(name, [])
                for found_node in found_nodes:
                    if found_node.lineno <= klass.lineno:
                        consumed.append((scope_locals, name))
                        found = True
                        break
            # Check parent scope
            nodes_in_parent_scope = parent_node.locals.get(name, [])
            for found_node_parent in nodes_in_parent_scope:
                if found_node_parent.lineno <= klass.lineno:
                    found = True
                    break
        if (
            not found
            and not metaclass
            and not (
                name in nodes.Module.scope_attrs
                or utils.is_builtin(name)
                or name in self.config.additional_builtins
            )
        ):
            self.add_message("undefined-variable", node=klass, args=(name,))

        return consumed


def register(linter: "PyLinter") -> None:
    linter.register_checker(VariablesChecker(linter))
