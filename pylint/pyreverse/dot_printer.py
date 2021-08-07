# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""
Class to generate files in dot format and image formats supported by Graphviz.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, FrozenSet, List, Optional

import astroid

from pylint.pyreverse.printer import EdgeType, Layout, NodeProperties, NodeType, Printer
from pylint.pyreverse.utils import check_graphviz_availability, get_annotation_label

ALLOWED_CHARSETS: FrozenSet[str] = frozenset(("utf-8", "iso-8859-1", "latin1"))
SHAPES: Dict[NodeType, str] = {
    NodeType.PACKAGE: "box",
    NodeType.INTERFACE: "record",
    NodeType.CLASS: "record",
}
ARROWS: Dict[EdgeType, Dict] = {
    EdgeType.INHERITS: dict(arrowtail="none", arrowhead="empty"),
    EdgeType.IMPLEMENTS: dict(arrowtail="node", arrowhead="empty", style="dashed"),
    EdgeType.ASSOCIATION: dict(
        fontcolor="green", arrowtail="none", arrowhead="diamond", style="solid"
    ),
    EdgeType.USES: dict(arrowtail="none", arrowhead="open"),
}


class DotPrinter(Printer):
    def __init__(
        self,
        title: str,
        layout: Optional[Layout] = None,
        use_automatic_namespace: Optional[bool] = None,
    ):
        self.charset = "utf-8"
        self.node_style = "solid"
        super().__init__(title, layout, use_automatic_namespace)

    def _open_graph(self) -> None:
        """Emit the header lines"""
        self.emit(f'digraph "{self.title}" {{')
        if self.layout:
            self.emit(f"rankdir={self.layout.value}")
        if self.charset:
            assert (
                self.charset.lower() in ALLOWED_CHARSETS
            ), f"unsupported charset {self.charset}"
            self.emit(f'charset="{self.charset}"')

    def emit_node(
        self,
        name: str,
        type_: NodeType,
        properties: Optional[NodeProperties] = None,
    ) -> None:
        """Create a new node. Nodes can be classes, packages, participants etc."""
        if properties is None:
            properties = NodeProperties(label=name)
        shape = SHAPES[type_]
        color = properties.color if properties.color is not None else "black"
        label = self._build_label_for_node(properties)
        if label:
            if type_ is NodeType.INTERFACE:
                label = "<<interface>>\\n" + label
            label_part = f', label="{label}"'
        else:
            label_part = ""
        fontcolor_part = (
            f', fontcolor="{properties.fontcolor}"' if properties.fontcolor else ""
        )
        self.emit(
            f'"{name}" [color="{color}"{fontcolor_part}{label_part}, shape="{shape}", style="{self.node_style}"];'
        )

    @staticmethod
    def _build_label_for_node(properties: NodeProperties) -> str:
        label = properties.label
        if label and properties.attrs is not None and properties.methods is not None:
            methods: List[str] = []
            for func in properties.methods:
                return_type = (
                    f": {get_annotation_label(func.returns)}" if func.returns else ""
                )

                if func.args.args:
                    arguments: List[astroid.AssignName] = [
                        arg for arg in func.args.args if arg.name != "self"
                    ]
                else:
                    arguments = []

                annotations = dict(zip(arguments, func.args.annotations[1:]))
                for arg in arguments:
                    annotation_label = ""
                    ann = annotations.get(arg)
                    if ann:
                        annotation_label = get_annotation_label(ann)
                    annotations[arg] = annotation_label

                args = ", ".join(
                    f"{arg.name}: {ann}" if ann else f"{arg.name}"
                    for arg, ann in annotations.items()
                )

                methods.append(fr"{func.name}({args}){return_type}\l")
            label = r"{{{}|{}\l|{}}}".format(
                label, r"\l".join(properties.attrs), "".join(methods)
            )
        return label

    def emit_edge(
        self,
        from_node: str,
        to_node: str,
        type_: EdgeType,
        label: Optional[str] = None,
    ) -> None:
        """Create an edge from one node to another to display relationships."""
        arrowstyle = ARROWS[type_]
        attrs = [f'{prop}="{value}"' for prop, value in arrowstyle.items()]
        if label:
            attrs.append(f'label="{label}"')
        self.emit(f'"{from_node}" -> "{to_node}" [{", ".join(sorted(attrs))}];')

    def generate(self, outputfile: str) -> None:
        self._close_graph()
        graphviz_extensions = ("dot", "gv")
        name = self.title
        if outputfile is None:
            target = "png"
            pdot, dot_sourcepath = tempfile.mkstemp(".gv", name)
            ppng, outputfile = tempfile.mkstemp(".png", name)
            os.close(pdot)
            os.close(ppng)
        else:
            target = Path(outputfile).suffix.lstrip(".")
            if not target:
                target = "png"
                outputfile = outputfile + "." + target
            if target not in graphviz_extensions:
                pdot, dot_sourcepath = tempfile.mkstemp(".gv", name)
                os.close(pdot)
            else:
                dot_sourcepath = outputfile
        with open(dot_sourcepath, "w", encoding="utf8") as outfile:
            outfile.writelines(self.lines)
        if target not in graphviz_extensions:
            check_graphviz_availability()
            use_shell = sys.platform == "win32"
            subprocess.call(
                ["dot", "-T", target, dot_sourcepath, "-o", outputfile],
                shell=use_shell,
            )
            os.unlink(dot_sourcepath)

    def _close_graph(self) -> None:
        """Emit the lines needed to properly close the graph."""
        self.emit("}\n")
