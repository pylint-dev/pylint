# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unit test for the diagrams modules."""

from __future__ import annotations

from collections.abc import Sequence

from pylint.pyreverse.diadefslib import DefaultDiadefGenerator, DiadefsHandler
from pylint.pyreverse.inspector import Linker
from pylint.testutils.pyreverse import PyreverseConfig
from pylint.typing import GetProjectCallable


def test_property_handling(
    default_config: PyreverseConfig,
    default_args: Sequence[str],
    get_project: GetProjectCallable,
) -> None:
    project = get_project("data.property_pattern")
    class_diagram = DefaultDiadefGenerator(
        Linker(project), DiadefsHandler(default_config, default_args)
    ).visit(project)[0]
    obj = class_diagram.classe("PropertyPatterns")
    assert len(class_diagram.get_methods(obj.node)) == 0
    assert class_diagram.get_attrs(obj.node) == ["prop1", "prop2"]
