# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

from enum import Enum
from typing import List, Optional, Union


class PumlItem(Enum):
    CLASS = "class"
    PACKAGE = "package"


class PumlArrow(Enum):
    INHERITS = "--|>"
    IMPLEMENTS = "..|>"
    ASSOCIATION = "--*"
    USES = "-->"


class PlantUmlPrinter:
    def __init__(self, title: str):
        self.title: str = title
        self.lines: List[str] = []
        self._begin()

    def _begin(self):
        self.emit("@startuml " + self.title)

    def emit(self, line: str):
        if not line.endswith("\n"):
            line += "\n"
        self.lines.append(line)

    def emit_node(
        self,
        id_: Union[int, str],
        type_: PumlItem,
        label: str,
        body: Optional[str] = "",
    ):
        self.emit(f'{type_.value} "{label}" as {id_} {{\n{body}\n}}')

    def emit_edge(
        self,
        from_node: Union[int, str],
        to_node: Union[int, str],
        type_: PumlArrow,
        label: Optional[str] = None,
    ):
        edge = f"{from_node} {type_.value} {to_node}"
        if label:
            edge += f" : {label}"
        self.emit(edge)

    def generate(self, outputfile: str):
        self._end()
        with open(outputfile, "w", encoding="utf-8") as outfile:
            outfile.writelines(self.lines)

    def _end(self):
        self.emit("@enduml")
