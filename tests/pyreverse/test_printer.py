# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

from typing import Type

import pytest

from pylint.pyreverse.dot_printer import DotPrinter
from pylint.pyreverse.printer import Layout, Printer
from pylint.pyreverse.vcg_printer import VCGPrinter


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
    ],
)
def test_explicit_layout(
    layout: Layout, printer_class: Type[Printer], expected_content: str, line_index: int
) -> None:
    printer = printer_class(title="unittest", layout=layout)
    assert printer.lines[line_index].strip() == expected_content
