# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import pytest
from astroid import nodes

from pylint.pyreverse.dot_printer import DotPrinter
from pylint.pyreverse.plantuml_printer import PlantUmlPrinter
from pylint.pyreverse.printer import Layout, NodeProperties, NodeType, Printer


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
    func = nodes.FunctionDef(
        name="func",
        lineno=1,
        col_offset=0,
        end_lineno=None,
        end_col_offset=None,
        parent=None,
    )
    args = nodes.Arguments(vararg=None, kwarg=None, parent=func)
    args.args = None
    func.postinit(args, body=None)
    parsed_args = Printer._get_method_arguments(func)
    assert parsed_args == []


class TestPlantUmlPrinter:
    printer = PlantUmlPrinter(title="unittest", layout=Layout.TOP_TO_BOTTOM)

    def test_node_without_properties(self) -> None:
        self.printer.emit_node(name="test", type_=NodeType.CLASS)
        assert self.printer.lines[-2:] == ['class "test" as test {\n', "}\n"]


def test_dot_printer_light_theme_has_no_bgcolor() -> None:
    printer = DotPrinter(title="unittest")
    assert not any("bgcolor" in line for line in printer.lines)


def test_dot_printer_dark_theme_emits_bgcolor_and_default_colors() -> None:
    printer = DotPrinter(title="unittest", theme="dark")
    assert any('bgcolor="#1e1e1e"' in line for line in printer.lines)
    printer.emit_node(name="test", type_=NodeType.CLASS)
    node_line = printer.lines[-1]
    assert 'color="#e0e0e0"' in node_line
    assert 'fontcolor="#e0e0e0"' in node_line


def test_dot_printer_node_color_override_takes_precedence_over_theme() -> None:
    printer = DotPrinter(title="unittest", theme="dark")
    printer.emit_node(
        name="test",
        type_=NodeType.CLASS,
        properties=NodeProperties(label="test", color="red", fontcolor="blue"),
    )
    node_line = printer.lines[-1]
    assert 'color="red"' in node_line
    assert 'fontcolor="blue"' in node_line


def test_plantuml_printer_light_theme_has_no_skinparam() -> None:
    printer = PlantUmlPrinter(title="unittest")
    assert not any("skinparam" in line for line in printer.lines)


def test_plantuml_printer_dark_theme_emits_skinparam_block() -> None:
    printer = PlantUmlPrinter(title="unittest", theme="dark")
    joined = "".join(printer.lines)
    assert "skinparam backgroundColor #1e1e1e" in joined
    assert "skinparam class {" in joined
    assert "FontColor #e0e0e0" in joined


def test_plantuml_printer_fontcolor_override_takes_precedence_over_theme() -> None:
    printer = PlantUmlPrinter(title="unittest", theme="dark")
    printer.emit_node(
        name="test",
        type_=NodeType.CLASS,
        properties=NodeProperties(label="test", fontcolor="red"),
    )
    assert any("<color:red>test</color>" in line for line in printer.lines)
