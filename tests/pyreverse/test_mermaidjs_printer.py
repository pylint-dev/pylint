# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from pylint.pyreverse.mermaidjs_printer import HTMLMermaidJSPrinter, MermaidJSPrinter


def test_html_mermaidjs_printer_light_theme_has_no_init_directive() -> None:
    printer = HTMLMermaidJSPrinter(title="unittest")
    assert not any("%%{init:" in line for line in printer.lines)


def test_html_mermaidjs_printer_dark_theme_emits_init_directive() -> None:
    printer = HTMLMermaidJSPrinter(title="unittest", theme="dark")
    assert any("%%{init: {'theme': 'dark'}}%%" in line for line in printer.lines)


def test_mermaidjs_printer_ignores_theme() -> None:
    """MermaidJSPrinter output may be embedded in a page with its own Mermaid
    theme configuration, so it intentionally never emits a theme directive.
    """
    light = MermaidJSPrinter(title="unittest", theme="light")
    dark = MermaidJSPrinter(title="unittest", theme="dark")
    assert light.lines == dark.lines
    assert not any("%%{init:" in line for line in dark.lines)
