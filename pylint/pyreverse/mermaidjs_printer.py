# Copyright (c) 2021 Antonio Quarta <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""
Class to generate files in mermaidjs format
"""
from typing import Dict, Optional

from pylint.pyreverse.printer import EdgeType, NodeProperties, NodeType, Printer
from pylint.pyreverse.utils import get_annotation_label


class MermaidJSPrinter(Printer):
    """Printer for MermaidJS diagrams"""

    DEFAULT_COLOR = "black"

    NODES: Dict[NodeType, str] = {
        NodeType.CLASS: "class",
        NodeType.INTERFACE: "class",
        NodeType.PACKAGE: "class",
    }
    ARROWS: Dict[EdgeType, str] = {
        EdgeType.INHERITS: "--|>",
        EdgeType.IMPLEMENTS: "..|>",
        EdgeType.ASSOCIATION: "--*",
        EdgeType.USES: "-->",
    }

    def _open_graph(self) -> None:
        """Emit the header lines"""
        self.emit("classDiagram ")
        self._inc_indent()

    def emit_node(
        self,
        name: str,
        type_: NodeType,
        properties: Optional[NodeProperties] = None,
    ) -> None:
        """Create a new node. Nodes can be classes, packages, participants etc."""
        if properties is None:
            properties = NodeProperties(label=name)
        stereotype = "~~Interface~~" if type_ is NodeType.INTERFACE else ""
        nodetype = self.NODES[type_]
        body = []
        if properties.attrs:
            body.extend(properties.attrs)
        if properties.methods:
            for func in properties.methods:
                args = self._get_method_arguments(func)
                line = f"{func.name}({', '.join(args)})"
                if func.returns:
                    line += " -> " + get_annotation_label(func.returns)
                body.append(line)
        name = name.split(".")[-1]
        self.emit(f"{nodetype} {name}{stereotype} {{")
        self._inc_indent()
        for line in body:
            self.emit(line)
        self._dec_indent()
        self.emit("}")

    def emit_edge(
        self,
        from_node: str,
        to_node: str,
        type_: EdgeType,
        label: Optional[str] = None,
    ) -> None:
        """Create an edge from one node to another to display relationships."""
        from_node = from_node.split(".")[-1]
        to_node = to_node.split(".")[-1]
        edge = f"{from_node} {self.ARROWS[type_]} {to_node}"
        if label:
            edge += f" : {label}"
        self.emit(edge)

    def _close_graph(self) -> None:
        """Emit the lines needed to properly close the graph."""
        self._dec_indent()
