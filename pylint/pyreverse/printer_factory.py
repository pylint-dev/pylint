# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors

from typing import Dict, Type

from pylint.pyreverse.dot_printer import DotPrinter
from pylint.pyreverse.mermaidjs_printer import HTMLMermaidJSPrinter, MermaidJSPrinter
from pylint.pyreverse.plantuml_printer import PlantUmlPrinter
from pylint.pyreverse.printer import Printer
from pylint.pyreverse.vcg_printer import VCGPrinter

filetype_to_printer: Dict[str, Type[Printer]] = {
    "vcg": VCGPrinter,
    "plantuml": PlantUmlPrinter,
    "puml": PlantUmlPrinter,
    "mmd": MermaidJSPrinter,
    "html": HTMLMermaidJSPrinter,
    "dot": DotPrinter,
}


def get_printer_for_filetype(filetype: str) -> Type[Printer]:
    return filetype_to_printer.get(filetype, DotPrinter)
