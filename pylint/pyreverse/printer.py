# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""
Base class defining the interface for a printer.
"""
from enum import Enum
from typing import List, NamedTuple, Optional


class NodeType(Enum):
    CLASS = "class"
    INTERFACE = "interface"
    PACKAGE = "package"


class EdgeType(Enum):
    INHERITS = "inherits"
    IMPLEMENTS = "implements"
    ASSOCIATION = "association"
    USES = "uses"


class Layout(Enum):
    LEFT_TO_RIGHT = "LR"
    RIGHT_TO_LEFT = "RL"
    TOP_TO_BOTTOM = "TB"
    BOTTOM_TO_TOP = "BT"


class NodeProperties(NamedTuple):
    label: str
    color: Optional[str] = None
    fontcolor: Optional[str] = None
    body: Optional[str] = None


class Printer:
    """Base class defining the interface for a printer"""

    def __init__(
        self,
        title: str,
        layout: Optional[Layout] = None,
        use_automatic_namespace: Optional[bool] = None,
    ):
        self.title: str = title
        self.layout = layout
        self.use_automatic_namespace = use_automatic_namespace
        self.lines: List[str] = []
        self._open_graph()

    def _open_graph(self) -> None:
        """Emit the header lines"""
        raise NotImplementedError

    def emit(self, line: str, force_newline: Optional[bool] = True) -> None:
        if force_newline and not line.endswith("\n"):
            line += "\n"
        self.lines.append(line)

    def emit_node(
        self,
        name: str,
        type_: NodeType,
        properties: Optional[NodeProperties] = None,
    ) -> None:
        """Create a new node. Nodes can be classes, packages, participants etc."""
        raise NotImplementedError

    def emit_edge(
        self,
        from_node: str,
        to_node: str,
        type_: EdgeType,
        label: Optional[str] = None,
    ) -> None:
        """Create an edge from one node to another to display relationships."""
        raise NotImplementedError

    def generate(self, outputfile: str) -> None:
        """Generate and save the final outputfile."""
        self._close_graph()
        with open(outputfile, "w", encoding="utf-8") as outfile:
            outfile.writelines(self.lines)

    def _close_graph(self) -> None:
        """Emit the lines needed to properly close the graph."""
        raise NotImplementedError
