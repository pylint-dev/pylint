# Copyright (c) 2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Takahide Nojima <nozzy123nozzy@gmail.com>
#
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unit test for the diagrams modules"""
from typing import Callable

from pylint.pyreverse.diadefslib import DefaultDiadefGenerator, DiadefsHandler
from pylint.pyreverse.inspector import Linker
from pylint.testutils.pyreverse import PyreverseConfig


def test_property_handling(
    default_config: PyreverseConfig, get_project: Callable
) -> None:
    project = get_project("data.property_pattern")
    class_diagram = DefaultDiadefGenerator(
        Linker(project), DiadefsHandler(default_config)
    ).visit(project)[0]
    obj = class_diagram.classe("PropertyPatterns")
    assert len(class_diagram.get_methods(obj.node)) == 0
    assert class_diagram.get_attrs(obj.node) == ["prop1", "prop2"]
