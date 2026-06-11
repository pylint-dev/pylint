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

    visit_asyncfunctiondef = visit_functiondef

    @staticmethod
    def _is_exempted(node: nodes.FunctionDef | nodes.AsyncFunctionDef) -> bool:
        """Return whether annotation checks should be skipped for ``node``.

        These exemptions are shared by the return-type and parameter checks:
        the signature is either inherited, generated, or intentionally
        annotation-free, so flagging it would only add noise.
        """
        if utils.decorated_with(node, ["abc.abstractmethod", "abc.abstractproperty"]):
            return True

        if utils.is_overload_stub(node):
            return True

        # ``@typing.override`` methods reuse the parent's signature; requiring
        # annotations on them would be redundant and noisy.
        if utils.decorated_with(
            node, ["typing.override", "typing_extensions.override"]
        ):
            return True

        return utils.is_property_setter_or_deleter(node)

    def _check_return_type_annotation(
        self, node: nodes.FunctionDef | nodes.AsyncFunctionDef
    ) -> None:
        """Check if a function has a return type annotation.

        Args:
            node: The function definition node to check
        """
        if node.returns is not None:
            return

        if node.type_comment_returns:
            return

        if node.name == "__init__":
            return

        if utils.decorated_with_property(node):
            return

        if self._is_exempted(node):
            return

        self.add_message("missing-return-type-annotation", node=node, args=(node.name,))

    def _check_param_type_annotations(
        self, node: nodes.FunctionDef | nodes.AsyncFunctionDef
    ) -> None:
        """Check if function parameters have type annotations.

        Args:
            node: The function definition node to check
        """
        if self._is_exempted(node):
            return

        arguments = node.args

        # In bound methods (instance and class methods) the first positional
        # parameter is the implicit ``self``/``cls`` and never needs an
        # annotation. Static methods and plain functions have no such parameter,
        # even when the first parameter happens to be named ``self``.
        skip_first = node.is_method() and node.type != "staticmethod"

        # Check positional-only args
        if arguments.posonlyargs:
            annotations = arguments.posonlyargs_annotations or []
            for idx, arg in enumerate(arguments.posonlyargs):
                if idx == 0 and skip_first:
                    continue
                if idx >= len(annotations) or annotations[idx] is None:
                    self.add_message(
                        "missing-param-type-annotation",
                        node=node,
                        args=(arg.name, node.name),
                    )
            # The implicit first parameter, if any, lives in posonlyargs.
            skip_first = False

        # Check regular args (skip self/cls for methods)
        if arguments.args:
            annotations = arguments.annotations or []
            for idx, arg in enumerate(arguments.args):
                if idx == 0 and skip_first:
                    continue
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
