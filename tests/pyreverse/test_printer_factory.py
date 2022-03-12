# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

"""Unit tests for pylint.pyreverse.printer_factory."""

import pytest

from pylint.pyreverse import printer_factory
from pylint.pyreverse.dot_printer import DotPrinter
from pylint.pyreverse.plantuml_printer import PlantUmlPrinter
from pylint.pyreverse.vcg_printer import VCGPrinter


@pytest.mark.parametrize(
    "filetype, expected_printer_class",
    [
        ("vcg", VCGPrinter),
        ("dot", DotPrinter),
        ("puml", PlantUmlPrinter),
        ("plantuml", PlantUmlPrinter),
        ("png", DotPrinter),
    ],
)
def test_get_printer_for_filetype(filetype, expected_printer_class):
    assert printer_factory.get_printer_for_filetype(filetype) == expected_printer_class
