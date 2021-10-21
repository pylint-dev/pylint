# Copyright (c) 2021 Takahide Nojima <nozzy123nozzy@gmail.com>
#
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unit test for the ClassDiagram modules"""
# pylint: disable=redefined-outer-name
from typing import Callable

import pytest

from pylint.pyreverse.diadefslib import DefaultDiadefGenerator, DiadefsHandler
from pylint.pyreverse.inspector import Linker
from pylint.testutils.pyreverse import PyreverseConfig


@pytest.fixture
def HANDLER(default_config: PyreverseConfig) -> DiadefsHandler:
    return DiadefsHandler(default_config)


def test_property_handling(HANDLER: DiadefsHandler, get_project: Callable) -> None:
    project = get_project("prop_data.property_pattern")
    cd = DefaultDiadefGenerator(Linker(project), HANDLER).visit(project)[0]
    obj = cd.classe("PropertyPatterns")
    assert len(cd.get_methods(obj.node)) == 0
    assert cd.get_attrs(obj.node) == ["prop1", "prop2", "prop3", "prop4"]
