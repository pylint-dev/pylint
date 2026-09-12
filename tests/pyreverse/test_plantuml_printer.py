# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from pylint.pyreverse.plantuml_printer import PlantUmlPrinter
from pylint.pyreverse.printer import Layout, NodeProperties, NodeType


class TestPlantUmlPrinter:
    printer = PlantUmlPrinter(title="unittest", layout=Layout.TOP_TO_BOTTOM)

    def test_node_without_properties(self) -> None:
        self.printer.emit_node(name="test", type_=NodeType.CLASS)
        assert self.printer.lines[-2:] == ['class "test" as test {\n', "}\n"]


def test_plantuml_printer_light_theme_has_no_skinparam() -> None:
    printer = PlantUmlPrinter(title="unittest")
    assert not any("skinparam" in line for line in printer.lines)


def test_plantuml_printer_dark_theme_emits_skinparam_block() -> None:
    printer = PlantUmlPrinter(title="unittest", theme="dark")
    joined = "".join(printer.lines)
    assert "skinparam backgroundColor #1e1e1e" in joined
    assert "skinparam class {" in joined
    assert "FontColor #e0e0e0" in joined


def test_plantuml_printer_dark_theme_sets_attribute_font_color() -> None:
    """FontColor only styles the class name; method/attribute text inside the
    class box is styled separately by AttributeFontColor and must also be set
    for the dark theme, or it defaults to unreadable black.
    """
    printer = PlantUmlPrinter(title="unittest", theme="dark")
    joined = "".join(printer.lines)
    assert "AttributeFontColor #e0e0e0" in joined


def test_plantuml_printer_fontcolor_override_takes_precedence_over_theme() -> None:
    printer = PlantUmlPrinter(title="unittest", theme="dark")
    printer.emit_node(
        name="test",
        type_=NodeType.CLASS,
        properties=NodeProperties(label="test", fontcolor="red"),
    )
    assert any("<color:red>test</color>" in line for line in printer.lines)
