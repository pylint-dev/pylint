# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

from typing import Type

import pytest

from pylint.pyreverse.printer import (
    DotPrinter,
    Layout,
    PlantUmlPrinter,
    Printer,
    VCGPrinter,
    get_printer_for_filetype,
)


@pytest.mark.parametrize(
    "filename, expected_printer_class",
    [
        ("dot", DotPrinter),
        ("png", DotPrinter),
        ("vcg", VCGPrinter),
        ("puml", PlantUmlPrinter),
    ],
)
def test_get_printer_for_filetype(
    filename: str, expected_printer_class: Type[Printer]
) -> None:
    returned_printer_class = get_printer_for_filetype(filename)
    assert returned_printer_class == expected_printer_class


@pytest.mark.parametrize(
    "layout, printer_class, expected_content, line_index",
    [
        (Layout.TOP_TO_BOTTOM, DotPrinter, "rankdir=TB", -2),
        (Layout.BOTTOM_TO_TOP, DotPrinter, "rankdir=BT", -2),
        (Layout.LEFT_TO_RIGHT, DotPrinter, "rankdir=LR", -2),
        (Layout.RIGHT_TO_LEFT, DotPrinter, "rankdir=RL", -2),
        (Layout.TOP_TO_BOTTOM, VCGPrinter, "orientation:top_to_bottom", -1),
        (Layout.BOTTOM_TO_TOP, VCGPrinter, "orientation:bottom_to_top", -1),
        (Layout.LEFT_TO_RIGHT, VCGPrinter, "orientation:left_to_right", -1),
        (Layout.RIGHT_TO_LEFT, VCGPrinter, "orientation:right_to_left", -1),
        (Layout.TOP_TO_BOTTOM, PlantUmlPrinter, "top to bottom direction", -1),
        (Layout.LEFT_TO_RIGHT, PlantUmlPrinter, "left to right direction", -1),
    ],
)
def test_explicit_layout(
    layout: Layout, printer_class: Type[Printer], expected_content: str, line_index: int
) -> None:
    printer = printer_class(title="unittest", layout=layout)
    assert printer.lines[line_index].strip() == expected_content


@pytest.mark.parametrize(
    "layout, printer_class",
    [
        (Layout.BOTTOM_TO_TOP, PlantUmlPrinter),
        (Layout.RIGHT_TO_LEFT, PlantUmlPrinter),
    ],
)
def test_unsupported_layouts(layout, printer_class):
    with pytest.raises(ValueError):
        printer_class(title="unittest", layout=layout)
