# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import pytest
from astroid import nodes

from pylint.pyreverse.dot_printer import DotPrinter
from pylint.pyreverse.plantuml_printer import PlantUmlPrinter
from pylint.pyreverse.printer import Layout, NodeType, Printer


@pytest.mark.parametrize(
    "layout, printer_class, expected_content, line_index",
    [
        (Layout.TOP_TO_BOTTOM, DotPrinter, "rankdir=TB", -2),
        (Layout.BOTTOM_TO_TOP, DotPrinter, "rankdir=BT", -2),
        (Layout.LEFT_TO_RIGHT, DotPrinter, "rankdir=LR", -2),
        (Layout.RIGHT_TO_LEFT, DotPrinter, "rankdir=RL", -2),
        (Layout.TOP_TO_BOTTOM, PlantUmlPrinter, "top to bottom direction", -1),
        (Layout.LEFT_TO_RIGHT, PlantUmlPrinter, "left to right direction", -1),
    ],
)
def test_explicit_layout(
    layout: Layout, printer_class: type[Printer], expected_content: str, line_index: int
) -> None:
    printer = printer_class(title="unittest", layout=layout)
    assert printer.lines[line_index].strip() == expected_content


@pytest.mark.parametrize(
    "layout, printer_class",
    [(Layout.BOTTOM_TO_TOP, PlantUmlPrinter), (Layout.RIGHT_TO_LEFT, PlantUmlPrinter)],
)
def test_unsupported_layout(layout: Layout, printer_class: type[Printer]) -> None:
    with pytest.raises(ValueError):
        printer_class(title="unittest", layout=layout)


def test_method_arguments_none() -> None:
    func = nodes.FunctionDef()
    args = nodes.Arguments()
    args.args = None
    func.postinit(args, body=None)
    parsed_args = Printer._get_method_arguments(func)
    assert parsed_args == []


class TestPlantUmlPrinter:
    printer = PlantUmlPrinter(title="unittest", layout=Layout.TOP_TO_BOTTOM)

    def test_node_without_properties(self) -> None:
        self.printer.emit_node(name="test", type_=NodeType.CLASS)
        assert self.printer.lines[-2:] == ['class "test" as test {\n', "}\n"]
