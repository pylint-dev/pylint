# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Checker for type annotations in function definitions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pylint import checkers
from pylint.checkers import utils

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class TypeAnnotationChecker(checkers.BaseChecker):
    """Checker for enforcing type annotations on functions and methods.

    This checker verifies that functions and methods have appropriate
    type annotations for return values and parameters.
    """

    name = "type-annotation"
    msgs = {
        "C3801": (
            "Missing return type annotation for function %r",
            "missing-return-type-annotation",
            "Used when a function or method does not have a return type annotation. "
            "Type annotations improve code readability and help with static type checking.",
        ),
        "C3802": (
            "Missing type annotation for parameter %r in function %r",
            "missing-param-type-annotation",
            "Used when a function or method parameter does not have a type annotation. "
            "Type annotations improve code readability and help with static type checking.",
        ),
    }

    @utils.only_required_for_messages(
        "missing-return-type-annotation", "missing-param-type-annotation"
    )
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Check for missing type annotations in regular functions."""
        self._check_return_type_annotation(node)
        self._check_param_type_annotations(node)

    @utils.only_required_for_messages(
        "missing-return-type-annotation", "missing-param-type-annotation"
    )
    def visit_asyncfunctiondef(self, node: nodes.AsyncFunctionDef) -> None:
        """Check for missing type annotations in async functions."""
        self._check_return_type_annotation(node)
        self._check_param_type_annotations(node)

    def _check_return_type_annotation(
        self, node: nodes.FunctionDef | nodes.AsyncFunctionDef
    ) -> None:
        """Check if a function has a return type annotation.

        Args:
            node: The function definition node to check
        """
        # Skip if function already has return type annotation
        if node.returns is not None:
            return

        # Skip if function has type comment with return type
        if node.type_comment_returns:
            return

        # Skip __init__ methods as they implicitly return None
        if node.name == "__init__":
            return

        # Skip abstract methods (often overridden with proper annotations)
        if utils.decorated_with(node, ["abc.abstractmethod", "abc.abstractproperty"]):
            return

        # Skip overload decorators (stub definitions)
        if utils.decorated_with(
            node, ["typing.overload", "typing_extensions.overload"]
        ):
            return

        # Skip property setters and delete methods (return value not meaningful)
        if utils.decorated_with(
            node, ["property", "*.setter", "*.deleter", "builtins.property"]
        ):
            return

        # Emit the message
        self.add_message("missing-return-type-annotation", node=node, args=(node.name,))

    def _check_param_type_annotations(
        self, node: nodes.FunctionDef | nodes.AsyncFunctionDef
    ) -> None:
        """Check if function parameters have type annotations.

        Args:
            node: The function definition node to check
        """
        # Skip abstract methods
        if utils.decorated_with(node, ["abc.abstractmethod", "abc.abstractproperty"]):
            return

        # Skip overload decorators
        if utils.decorated_with(
            node, ["typing.overload", "typing_extensions.overload"]
        ):
            return

        arguments = node.args

        # Check positional-only args
        if arguments.posonlyargs:
            annotations = arguments.posonlyargs_annotations or []
            for idx, arg in enumerate(arguments.posonlyargs):
                if arg.name in {"self", "cls"}:
                    continue
                if idx >= len(annotations) or annotations[idx] is None:
                    self.add_message(
                        "missing-param-type-annotation",
                        node=node,
                        args=(arg.name, node.name),
                    )

        # Check regular args (skip self/cls for methods)
        if arguments.args:
            annotations = arguments.annotations or []
            start_idx = 0
            # Skip 'self' or 'cls' for methods
            if (
                arguments.args
                and arguments.args[0].name in {"self", "cls"}
                and isinstance(node.parent, nodes.ClassDef)
            ):
                start_idx = 1

            for idx, arg in enumerate(arguments.args[start_idx:], start=start_idx):
                if idx >= len(annotations) or annotations[idx] is None:
                    self.add_message(
                        "missing-param-type-annotation",
                        node=node,
                        args=(arg.name, node.name),
                    )

        # Check *args
        if arguments.vararg and not arguments.varargannotation:
            self.add_message(
                "missing-param-type-annotation",
                node=node,
                args=(arguments.vararg, node.name),
            )

        # Check keyword-only args
        if arguments.kwonlyargs:
            annotations = arguments.kwonlyargs_annotations or []
            for idx, arg in enumerate(arguments.kwonlyargs):
                if idx >= len(annotations) or annotations[idx] is None:
                    self.add_message(
                        "missing-param-type-annotation",
                        node=node,
                        args=(arg.name, node.name),
                    )

        # Check **kwargs
        if arguments.kwarg and not arguments.kwargannotation:
            self.add_message(
                "missing-param-type-annotation",
                node=node,
                args=(arguments.kwarg, node.name),
            )


def register(linter: PyLinter) -> None:
    """Register the checker with the linter."""
    linter.register_checker(TypeAnnotationChecker(linter))
