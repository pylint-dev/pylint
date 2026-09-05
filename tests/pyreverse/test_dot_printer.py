# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from pylint.pyreverse.dot_printer import DotPrinter
from pylint.pyreverse.printer import EdgeType, NodeProperties, NodeType


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


def test_dot_printer_light_theme_edge_color() -> None:
    printer = DotPrinter(title="unittest")
    printer.emit_edge(from_node="a", to_node="b", type_=EdgeType.USES)
    assert 'color="black"' in printer.lines[-1]


def test_dot_printer_dark_theme_edge_color() -> None:
    printer = DotPrinter(title="unittest", theme="dark")
    printer.emit_edge(from_node="a", to_node="b", type_=EdgeType.USES)
    assert 'color="#e0e0e0"' in printer.lines[-1]


def test_dot_printer_dark_theme_edge_color_with_per_type_override() -> None:
    printer = DotPrinter(title="unittest", theme="dark")
    printer.emit_edge(from_node="a", to_node="b", type_=EdgeType.COMPOSITION)
    edge_line = printer.lines[-1]
    assert 'color="#e0e0e0"' in edge_line
    assert 'fontcolor="green"' in edge_line
