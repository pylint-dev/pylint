# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from pylint.pyreverse.mermaidjs_printer import HTMLMermaidJSPrinter, MermaidJSPrinter


def test_html_mermaidjs_printer_light_theme_has_no_frontmatter() -> None:
    printer = HTMLMermaidJSPrinter(title="unittest")
    assert not any(line.strip() == "---" for line in printer.lines)


def test_html_mermaidjs_printer_dark_theme_emits_frontmatter() -> None:
    printer = HTMLMermaidJSPrinter(title="unittest", theme="dark")
    stripped_lines = [line.strip() for line in printer.lines]
    assert stripped_lines.count("---") == 2
    assert "config:" in stripped_lines
    assert "theme: dark" in stripped_lines
    # The frontmatter delimiters and config key must be unindented, even
    # though they're emitted from inside the indented HTML boilerplate.
    assert "---\n" in printer.lines
    assert "config:\n" in printer.lines


def test_html_mermaidjs_printer_close_graph_dedents_class_diagram_block() -> None:
    printer = HTMLMermaidJSPrinter(title="unittest")
    printer._close_graph()
    assert printer._indent == ""


def test_mermaidjs_printer_ignores_theme() -> None:
    """MermaidJSPrinter output may be embedded in a page with its own Mermaid
    theme configuration, so it intentionally never emits a theme directive.
    """
    light = MermaidJSPrinter(title="unittest", theme="light")
    dark = MermaidJSPrinter(title="unittest", theme="dark")
    assert light.lines == dark.lines
    assert not any("%%{init:" in line for line in dark.lines)
