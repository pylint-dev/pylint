# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Check that the text of a node stays readable on its background.

The other theme tests check that a given color is emitted. These check the
result instead: whatever the theme and the fill color of a node, the color of
its text has to contrast with what is behind it.
"""

from __future__ import annotations

import re
from collections.abc import Callable

import pytest

from pylint.pyreverse.dot_printer import DotPrinter
from pylint.pyreverse.main import DEFAULT_COLOR_PALETTE
from pylint.pyreverse.mermaidjs_printer import HTMLMermaidJSPrinter
from pylint.pyreverse.plantuml_printer import PlantUmlPrinter
from pylint.pyreverse.printer import NodeProperties, NodeType, Printer

# Minimum contrast ratio for normal text in WCAG 2.1, level AA
MIN_CONTRAST_RATIO = 4.5
NAMED_COLORS = {"black": "#000000", "white": "#ffffff", "grey": "#808080"}
# "grey" is what ``DiagramWriter.get_shape_color`` uses for the stdlib
FILL_COLORS = (None, "grey", *DEFAULT_COLOR_PALETTE)
# What a renderer falls back to when pyreverse does not emit a color
DEFAULT_FONT_COLORS = {"light": "black", "dark": "#e0e0e0"}
DEFAULT_BACKGROUND_COLORS = {"light": "white", "dark": "#1e1e1e"}


def _luminance(color: str) -> float:
    hex_color = NAMED_COLORS.get(color, color).lstrip("#")
    channels = [int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    red, green, blue = (
        c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels
    )
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def _contrast_ratio(color: str, other_color: str) -> float:
    lighter, darker = sorted((_luminance(color), _luminance(other_color)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def _dot_colors(lines: list[str]) -> tuple[str | None, str | None]:
    node = lines[-1]
    font = re.search(r'fontcolor="([^"]+)"', node)
    fill = re.search(r' \[color="([^"]+)"', node) if 'style="filled"' in node else None
    return (font.group(1) if font else None, fill.group(1) if fill else None)


def _plantuml_colors(lines: list[str]) -> tuple[str | None, str | None]:
    node = next(line for line in reversed(lines) if line.startswith("class "))
    match = re.search(r" as node(?: #(\w+))?(?:;text:(\w+))? \{", node)
    assert match
    fill, font = match.groups()
    # PlantUML prefixes every color with a hash, named ones included
    if fill and fill not in NAMED_COLORS:
        fill = f"#{fill}"
    return (font, fill)


def _mermaid_colors(lines: list[str]) -> tuple[str | None, str | None]:
    match = re.search(r"style node fill:([^,\s]+)(?:,color:(\S+))?", lines[-1])
    if not match:
        return (None, None)
    fill, font = match.groups()
    return (font, fill)


@pytest.mark.parametrize("fill", FILL_COLORS)
@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize(
    "printer_class,get_colors",
    [
        (DotPrinter, _dot_colors),
        (PlantUmlPrinter, _plantuml_colors),
        (HTMLMermaidJSPrinter, _mermaid_colors),
    ],
)
def test_node_text_is_readable_on_its_background(
    printer_class: type[Printer],
    get_colors: Callable[[list[str]], tuple[str | None, str | None]],
    theme: str,
    fill: str | None,
) -> None:
    printer = printer_class(title="unittest", theme=theme)
    printer.emit_node(
        name="node",
        type_=NodeType.CLASS,
        properties=NodeProperties(label="node", attrs=["attribute"], color=fill),
    )
    font, background = get_colors(printer.lines)
    font = font or DEFAULT_FONT_COLORS[theme]
    background = background or DEFAULT_BACKGROUND_COLORS[theme]
    ratio = _contrast_ratio(font, background)
    assert ratio >= MIN_CONTRAST_RATIO, (
        f"{font} text on a {background} background has a contrast ratio of "
        f"{ratio:.2f}, below {MIN_CONTRAST_RATIO}"
    )
