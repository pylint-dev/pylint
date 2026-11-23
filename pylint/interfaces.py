# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import warnings
from typing import NamedTuple

__all__ = (
    "CONFIDENCE_LEVELS",
    "CONFIDENCE_LEVEL_NAMES",
    "CONTROL_FLOW",
    "HIGH",
    "INFERENCE",
    "INFERENCE_FAILURE",
    "UNDEFINED",
)


class Confidence(NamedTuple):
    name: str
    description: str


# Warning Certainties
HIGH = Confidence("HIGH", "Warning that is not based on inference result.")
CONTROL_FLOW = Confidence(
    "CONTROL_FLOW", "Warning based on assumptions about control flow."
)
INFERENCE = Confidence("INFERENCE", "Warning based on inference result.")
INFERENCE_FAILURE = Confidence(
    "INFERENCE_FAILURE", "Warning based on inference with failures."
)
UNDEFINED = Confidence("UNDEFINED", "Warning without any associated confidence level.")

CONFIDENCE_LEVELS = [HIGH, CONTROL_FLOW, INFERENCE, INFERENCE_FAILURE, UNDEFINED]
CONFIDENCE_LEVEL_NAMES = [i.name for i in CONFIDENCE_LEVELS]
CONFIDENCE_MAP = {i.name: i for i in CONFIDENCE_LEVELS}


def _confidence_or_undefined(
    confidence: Confidence | None, stacklevel: int
) -> Confidence:
    """Turn the deprecated ``confidence=None`` into ``UNDEFINED``."""
    if confidence is not None:
        return confidence
    warnings.warn(
        "Passing 'confidence=None' is deprecated and will raise an error in "
        "pylint 5.0. Use 'pylint.interfaces.UNDEFINED' or omit the argument.",
        DeprecationWarning,
        stacklevel=stacklevel + 1,
    )
    return UNDEFINED
