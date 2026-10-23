# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Every message emitted on a node with an async form must decide about it.

The AST walker dispatches on the exact class name of a node, so ``visit_for``
never receives an ``AsyncFor`` even though ``AsyncFor`` is a subclass of
``For``. A checker has to add ``visit_asyncfor = visit_for`` explicitly, and
forgetting it silently skips all async code.

The decision is per message, not per visitor: when only some of the messages of
a visitor apply to the async form, the async visitor calls only those checks.
This test makes the choice explicit: every message of a sync visitor is also
declared by its async counterpart, or is listed below with the reason why not.
"""

from __future__ import annotations

from collections.abc import Callable

from astroid import nodes

from pylint import checkers, extensions
from pylint.lint import PyLinter

NODE_CLASSES = {cls for cls in nodes.ALL_NODE_CLASSES if isinstance(cls, type)}

# The lowercase name of each async node class, mapped to its sync base: e.g.
# ``asyncfor`` to ``for``.
ASYNC_TO_SYNC = {
    cls.__name__.lower(): base.__name__.lower()
    for cls in NODE_CLASSES
    for base in cls.__bases__
    if base in NODE_CLASSES and cls.__name__ == f"Async{base.__name__}"
}

# Stands for every message of a visitor not decorated with
# ``only_required_for_messages``.
ALL_MESSAGES = "*"

# The message cannot apply to the async form.
SYNC_ONLY = {
    ("ImportsChecker", "visit_for", ALL_MESSAGES): (
        "only module level statements are tracked, where 'async for' is a syntax error"
    ),
    **{
        ("ModifiedIterationChecker", "visit_for", message): (
            "a list, dict or set modified while iterated is never an async iterable"
        )
        for message in (
            "modified-iterating-dict",
            "modified-iterating-list",
            "modified-iterating-set",
        )
    },
    **{
        ("RecommendationChecker", "visit_for", message): (
            "range(), dict and set iteration, none of which is an async iterable"
        )
        for message in (
            "consider-using-dict-items",
            "consider-using-enumerate",
            "use-sequence-for-iteration",
        )
    },
    ("ThreadingChecker", "visit_with", "useless-with-lock"): (
        "threading locks are not asynchronous context managers"
    ),
    ("TypeChecker", "visit_for", "dict-items-missing-iter"): (
        "iterates a dict, which is not an async iterable"
    ),
    ("TypeChecker", "visit_with", "not-context-manager"): (
        "checks __enter__ and __exit__, AsyncChecker.visit_asyncwith checks the "
        "async protocol"
    ),
    ("TypeChecker", "visit_with", "async-context-manager-with-regular-with"): (
        "only means something for a regular 'with'"
    ),
    ("CodeStyleChecker", "visit_for", "consider-using-tuple"): (
        "iterates a list literal, which is not an async iterable"
    ),
    ("ConsiderUsingAnyOrAllChecker", "visit_for", "consider-using-any-or-all"): (
        "any() and all() cannot consume an async iterable"
    ),
}

# The message should also be emitted on the async form, but is not yet. Remove
# the entry when adding the async visitor.
NOT_YET_ASYNC = {
    ("RefactoringChecker", "visit_functiondef", ALL_MESSAGES): (
        "collects the return statements for inconsistent-return-statements"
    ),
    **{
        ("RefactoringChecker", "leave_functiondef", message): (
            "skips 'async def', and too-many-nested-blocks in an 'async def' is "
            "only reported when a later function flushes it"
        )
        for message in (
            "consider-using-with",
            "inconsistent-return-statements",
            "too-many-nested-blocks",
            "useless-return",
        )
    },
    ("DunderChecker", "visit_functiondef", ALL_MESSAGES): (
        "bad-dunder-name skips 'async def'"
    ),
    ("RepeatedIteratorLoopChecker", "visit_for", "looping-through-iterator"): (
        "an async generator is also exhausted after one loop"
    ),
    ("RepeatedIteratorLoopChecker", "leave_for", "looping-through-iterator"): (
        "pairs with visit_for"
    ),
}


def _messages(visitor: Callable[..., None] | None) -> set[str]:
    if visitor is None:
        return set()
    return set(getattr(visitor, "checks_msgs", ())) or {ALL_MESSAGES}


def test_every_message_decides_about_the_async_form() -> None:
    linter = PyLinter()
    checkers.initialize(linter)
    extensions.initialize(linter)
    without_async_form = set()
    for checker in linter.get_checkers():
        for async_name, sync_name in ASYNC_TO_SYNC.items():
            for prefix in ("visit", "leave"):
                sync_visitor = f"{prefix}_{sync_name}"
                sync_messages = _messages(getattr(checker, sync_visitor, None))
                async_messages = _messages(
                    getattr(checker, f"{prefix}_{async_name}", None)
                )
                if ALL_MESSAGES in async_messages:
                    continue
                without_async_form |= {
                    (type(checker).__name__, sync_visitor, message)
                    for message in sync_messages - async_messages
                }
    # Add the async visitor (e.g. ``visit_asyncfor = visit_for``), or list the
    # message in SYNC_ONLY or NOT_YET_ASYNC. An entry that is listed but not
    # reported anymore must be removed from its list.
    assert without_async_form == SYNC_ONLY.keys() | NOT_YET_ASYNC.keys()


def test_async_forms_are_found() -> None:
    assert ASYNC_TO_SYNC == {
        "asyncfor": "for",
        "asyncwith": "with",
        "asyncfunctiondef": "functiondef",
    }
