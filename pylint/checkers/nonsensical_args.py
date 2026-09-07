# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Checker for arguments that are never meaningful as infinity or NaN."""

from __future__ import annotations

import math
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple

import astroid
from astroid import nodes

from pylint.checkers import utils
from pylint.checkers.base_checker import BaseChecker
from pylint.checkers.utils import safe_infer
from pylint.interfaces import INFERENCE
from pylint.typing import MessageDefinitionTuple

if TYPE_CHECKING:
    from pylint.lint import PyLinter

ACCEPTABLE_NODES = (
    astroid.BoundMethod,
    astroid.UnboundMethod,
    nodes.FunctionDef,
    nodes.ClassDef,
)


class NonsensicalArgument(NamedTuple):
    """An argument that should never be given infinity or NaN.

    ``position`` is the index of the argument when it is passed positionally,
    counting from zero and ignoring ``self``, or None when the argument is
    keyword-only. ``name`` is the keyword it is passed under.

    ``on_inf`` and ``on_nan`` describe what goes wrong for each value, and are
    used as the tail of the emitted message. A value of None means that value
    is legitimate for this argument, so leaving both as None disables the
    entry.
    """

    position: int | None
    name: str
    on_inf: str | None = None
    on_nan: str | None = None


def _non_finite_value(node: nodes.NodeNG) -> float | None:
    """Return the infinity or NaN that `node` evaluates to, else None.

    ``float("inf")`` infers to an instance of float rather than to a constant,
    so the call has to be read directly. Every other spelling, ``math.inf``,
    ``math.nan``, a ``1e999`` literal or a name bound to one of those, is
    handled by inference.
    """
    match node:
        case nodes.Call(args=[nodes.Const(value=str() as text)]) if (
            isinstance(inferred := safe_infer(node.func), nodes.ClassDef)
            and inferred.qname() == "builtins.float"
        ):
            try:
                literal = float(text)
            except ValueError:
                return None
            return None if math.isfinite(literal) else literal

    inferred_value = safe_infer(node)
    if (
        isinstance(inferred_value, nodes.Const)
        and isinstance(inferred_value.value, float)
        and not math.isfinite(inferred_value.value)
    ):
        return inferred_value.value
    return None


class NonsensicalArgumentsMixin(BaseChecker):
    """A mixin implementing logic for arguments that must be finite.

    A class implementing this mixin must define the "nonsensical-float-arg"
    message, which it can do by unpacking ``NONSENSICAL_ARGUMENT_MESSAGE`` into
    its own ``msgs``, and should override :meth:`nonsensical_arguments`.

    A checker that defines its own ``visit_call`` must call
    :meth:`check_nonsensical_arguments` from it, as its own definition shadows
    the one provided here.
    """

    NONSENSICAL_ARGUMENT_MESSAGE: dict[str, MessageDefinitionTuple] = {
        "W3801": (
            "%s passed as %r to %s(), %s",
            "nonsensical-float-arg",
            "Some arguments have no meaningful behaviour for infinity or NaN. "
            "An infinite tolerance makes a comparison succeed whatever it is "
            "given, and an infinite timeout is rejected rather than waiting "
            "forever, so passing one is a mistake even when no exception is "
            "raised.",
            {"shared": True},
        ),
    }

    def nonsensical_arguments(self, qname: str) -> Iterable[NonsensicalArgument]:
        """Callback returning the arguments of `qname` that must be finite.

        Args:
            qname (str): qualified name of the called function, method or class

        Returns:
            collections.abc.Iterable of NonsensicalArgument, at most one per
            argument of `qname`.
        """
        # pylint: disable=unused-argument
        return ()

    @utils.only_required_for_messages("nonsensical-float-arg")
    def visit_call(self, node: nodes.Call) -> None:
        """Called when a :class:`nodes.Call` node is visited."""
        self.check_nonsensical_arguments(node)

    def check_nonsensical_arguments(self, node: nodes.Call) -> None:
        """Check the call for arguments that should not be infinity or NaN.

        This method should be called from the checker implementing this mixin.
        """
        inferred = safe_infer(node.func)
        if not isinstance(inferred, ACCEPTABLE_NODES):
            return

        keywords = {
            keyword.arg: keyword.value
            for keyword in node.keywords or ()
            if keyword.arg is not None
        }
        for argument in self.nonsensical_arguments(inferred.qname()):
            passed = keywords.get(argument.name)
            if passed is None:
                if argument.position is None or argument.position >= len(node.args):
                    continue
                passed = node.args[argument.position]

            value = _non_finite_value(passed)
            if value is None:
                continue
            consequence = argument.on_nan if math.isnan(value) else argument.on_inf
            if consequence is None:
                continue
            self.add_message(
                "nonsensical-float-arg",
                node=passed,
                args=(
                    passed.as_string(),
                    argument.name,
                    node.func.as_string(),
                    consequence,
                ),
                confidence=INFERENCE,
            )


# An infinite tolerance widens an approximate comparison until everything
# matches it, and a NaN tolerance makes every comparison but an exact one fail.
# A negative infinity is rejected outright rather than matching nothing, hence
# the deliberately unspecific wording for infinity.
_TOLERANCE = (
    "an infinite tolerance makes the comparison meaningless",
    "a NaN tolerance makes the comparison fail unless the values are equal",
)
# assertNotAlmostEqual inverts the test, so the same tolerance breaks it the
# other way around.
_INVERTED_TOLERANCE = (
    "an infinite tolerance makes the assertion meaningless",
    "a NaN tolerance makes the assertion fail whatever it is given",
)
# Timeouts are converted to a deadline in C, which infinity and NaN overflow.
# The conversion only happens once the call actually has to wait, so the same
# argument can raise on an empty queue and pass on a full one.
_TIMEOUT = (
    "an infinite timeout is not supported, omit the argument to wait forever",
    "a NaN timeout is not supported, omit the argument to wait forever",
)
# Anything converting a float to an integer, directly or through a ratio.
_INTEGER = (
    "infinity cannot be converted to an integer",
    "NaN cannot be converted to an integer",
)

NONSENSICAL_ARGUMENTS: dict[str, tuple[NonsensicalArgument, ...]] = {
    "math.isclose": (
        NonsensicalArgument(None, "rel_tol", *_TOLERANCE),
        NonsensicalArgument(None, "abs_tol", *_TOLERANCE),
    ),
    "cmath.isclose": (
        NonsensicalArgument(None, "rel_tol", *_TOLERANCE),
        NonsensicalArgument(None, "abs_tol", *_TOLERANCE),
    ),
    "unittest.case.TestCase.assertAlmostEqual": (
        NonsensicalArgument(4, "delta", *_TOLERANCE),
    ),
    "unittest.case.TestCase.assertNotAlmostEqual": (
        NonsensicalArgument(4, "delta", *_INVERTED_TOLERANCE),
    ),
    "time.sleep": (NonsensicalArgument(0, "secs", *_TIMEOUT),),
    "_socket.socket.settimeout": (NonsensicalArgument(0, "value", *_TIMEOUT),),
    "threading.lock.acquire": (NonsensicalArgument(1, "timeout", *_TIMEOUT),),
    "threading.Event.wait": (NonsensicalArgument(0, "timeout", *_TIMEOUT),),
    "threading.Condition.wait": (NonsensicalArgument(0, "timeout", *_TIMEOUT),),
    "queue.Queue.get": (NonsensicalArgument(1, "timeout", *_TIMEOUT),),
    "queue.Queue.put": (NonsensicalArgument(2, "timeout", *_TIMEOUT),),
    "builtins.int": (NonsensicalArgument(0, "x", *_INTEGER),),
    "math.floor": (NonsensicalArgument(0, "x", *_INTEGER),),
    "math.ceil": (NonsensicalArgument(0, "x", *_INTEGER),),
    "math.trunc": (NonsensicalArgument(0, "x", *_INTEGER),),
    "fractions.Fraction": (NonsensicalArgument(0, "numerator", *_INTEGER),),
}
# datetime is implemented twice, and the pure Python one is what astroid reads.
for _timedelta in ("datetime.timedelta", "_pydatetime.timedelta"):
    NONSENSICAL_ARGUMENTS[_timedelta] = tuple(
        NonsensicalArgument(_position, _unit, *_INTEGER)
        for _position, _unit in enumerate(
            (
                "days",
                "seconds",
                "microseconds",
                "milliseconds",
                "minutes",
                "hours",
                "weeks",
            )
        )
    )
for _fromtimestamp in (
    "datetime.datetime.fromtimestamp",
    "_pydatetime.datetime.fromtimestamp",
):
    NONSENSICAL_ARGUMENTS[_fromtimestamp] = (
        NonsensicalArgument(
            0,
            "timestamp",
            "infinity is outside the range of representable dates",
            "NaN is not a date",
        ),
    )


class NonsensicalArgumentsChecker(NonsensicalArgumentsMixin, BaseChecker):
    """Checks the standard library for arguments given infinity or NaN."""

    name = "nonsensical_arguments"
    msgs: dict[str, MessageDefinitionTuple] = {
        **NonsensicalArgumentsMixin.NONSENSICAL_ARGUMENT_MESSAGE,
    }

    def nonsensical_arguments(self, qname: str) -> Iterable[NonsensicalArgument]:
        return NONSENSICAL_ARGUMENTS.get(qname, ())


def register(linter: PyLinter) -> None:
    linter.register_checker(NonsensicalArgumentsChecker(linter))
