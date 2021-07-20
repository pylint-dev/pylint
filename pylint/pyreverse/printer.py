# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Florian Bruhin <me@the-compiler.org>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2020-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2020 Ram Rachum <ram@rachum.com>
# Copyright (c) 2020 谭九鼎 <109224573@qq.com>
# Copyright (c) 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""
Collection of printer classes for diagrams.
Printers are responsible for generating files that can be understood by tools like
Graphviz or PlantUML for example.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from enum import Enum
from typing import Any, Dict, FrozenSet, List, Mapping, NamedTuple, Optional, Tuple

from pylint.pyreverse.utils import get_file_extension


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


class VCGPrinter(Printer):
    SHAPES: Dict[NodeType, str] = {
        NodeType.PACKAGE: "box",
        NodeType.CLASS: "box",
        NodeType.INTERFACE: "ellipse",
    }
    ARROWS: Dict[EdgeType, Dict] = {
        EdgeType.USES: dict(arrowstyle="solid", backarrowstyle="none", backarrowsize=0),
        EdgeType.INHERITS: dict(
            arrowstyle="solid", backarrowstyle="none", backarrowsize=10
        ),
        EdgeType.IMPLEMENTS: dict(
            arrowstyle="solid",
            backarrowstyle="none",
            linestyle="dotted",
            backarrowsize=10,
        ),
        EdgeType.ASSOCIATION: dict(
            arrowstyle="solid", backarrowstyle="none", textcolor="green"
        ),
    }
    ORIENTATION: Dict[Layout, str] = {
        Layout.LEFT_TO_RIGHT: "left_to_right",
        Layout.RIGHT_TO_LEFT: "right_to_left",
        Layout.TOP_TO_BOTTOM: "top_to_bottom",
        Layout.BOTTOM_TO_TOP: "bottom_to_top",
    }
    ATTRS_VAL: Dict[str, Tuple] = {
        "algos": (
            "dfs",
            "tree",
            "minbackward",
            "left_to_right",
            "right_to_left",
            "top_to_bottom",
            "bottom_to_top",
            "maxdepth",
            "maxdepthslow",
            "mindepth",
            "mindepthslow",
            "mindegree",
            "minindegree",
            "minoutdegree",
            "maxdegree",
            "maxindegree",
            "maxoutdegree",
        ),
        "booleans": ("yes", "no"),
        "colors": (
            "black",
            "white",
            "blue",
            "red",
            "green",
            "yellow",
            "magenta",
            "lightgrey",
            "cyan",
            "darkgrey",
            "darkblue",
            "darkred",
            "darkgreen",
            "darkyellow",
            "darkmagenta",
            "darkcyan",
            "gold",
            "lightblue",
            "lightred",
            "lightgreen",
            "lightyellow",
            "lightmagenta",
            "lightcyan",
            "lilac",
            "turquoise",
            "aquamarine",
            "khaki",
            "purple",
            "yellowgreen",
            "pink",
            "orange",
            "orchid",
        ),
        "shapes": ("box", "ellipse", "rhomb", "triangle"),
        "textmodes": ("center", "left_justify", "right_justify"),
        "arrowstyles": ("solid", "line", "none"),
        "linestyles": ("continuous", "dashed", "dotted", "invisible"),
    }

    # meaning of possible values:
    #   O    -> string
    #   1    -> int
    #   list -> value in list
    GRAPH_ATTRS: Dict[str, Any] = {
        "title": 0,
        "label": 0,
        "color": ATTRS_VAL["colors"],
        "textcolor": ATTRS_VAL["colors"],
        "bordercolor": ATTRS_VAL["colors"],
        "width": 1,
        "height": 1,
        "borderwidth": 1,
        "textmode": ATTRS_VAL["textmodes"],
        "shape": ATTRS_VAL["shapes"],
        "shrink": 1,
        "stretch": 1,
        "orientation": ATTRS_VAL["algos"],
        "vertical_order": 1,
        "horizontal_order": 1,
        "xspace": 1,
        "yspace": 1,
        "layoutalgorithm": ATTRS_VAL["algos"],
        "late_edge_labels": ATTRS_VAL["booleans"],
        "display_edge_labels": ATTRS_VAL["booleans"],
        "dirty_edge_labels": ATTRS_VAL["booleans"],
        "finetuning": ATTRS_VAL["booleans"],
        "manhattan_edges": ATTRS_VAL["booleans"],
        "smanhattan_edges": ATTRS_VAL["booleans"],
        "port_sharing": ATTRS_VAL["booleans"],
        "edges": ATTRS_VAL["booleans"],
        "nodes": ATTRS_VAL["booleans"],
        "splines": ATTRS_VAL["booleans"],
    }
    NODE_ATTRS: Dict[str, Any] = {
        "title": 0,
        "label": 0,
        "color": ATTRS_VAL["colors"],
        "textcolor": ATTRS_VAL["colors"],
        "bordercolor": ATTRS_VAL["colors"],
        "width": 1,
        "height": 1,
        "borderwidth": 1,
        "textmode": ATTRS_VAL["textmodes"],
        "shape": ATTRS_VAL["shapes"],
        "shrink": 1,
        "stretch": 1,
        "vertical_order": 1,
        "horizontal_order": 1,
    }
    EDGE_ATTRS: Dict[str, Any] = {
        "sourcename": 0,
        "targetname": 0,
        "label": 0,
        "linestyle": ATTRS_VAL["linestyles"],
        "class": 1,
        "thickness": 0,
        "color": ATTRS_VAL["colors"],
        "textcolor": ATTRS_VAL["colors"],
        "arrowcolor": ATTRS_VAL["colors"],
        "backarrowcolor": ATTRS_VAL["colors"],
        "arrowsize": 1,
        "backarrowsize": 1,
        "arrowstyle": ATTRS_VAL["arrowstyles"],
        "backarrowstyle": ATTRS_VAL["arrowstyles"],
        "textmode": ATTRS_VAL["textmodes"],
        "priority": 1,
        "anchor": 1,
        "horizontal_order": 1,
    }

    def __init__(
        self,
        title: str,
        layout: Optional[Layout] = None,
        use_automatic_namespace: Optional[bool] = None,
    ):
        self._indent = ""
        super().__init__(title, layout, use_automatic_namespace)

    def _inc_indent(self) -> None:
        self._indent += "  "

    def _dec_indent(self) -> None:
        self._indent = self._indent[:-2]

    def _open_graph(self) -> None:
        """Emit the header lines"""
        self.emit(f"{self._indent}graph:{{\n")
        self._inc_indent()
        self._write_attributes(
            self.GRAPH_ATTRS,
            title=self.title,
            layoutalgorithm="dfs",
            late_edge_labels="yes",
            port_sharing="no",
            manhattan_edges="yes",
        )
        if self.layout:
            self._write_attributes(
                self.GRAPH_ATTRS, orientation=self.ORIENTATION[self.layout]
            )

    def emit_node(
        self,
        name: str,
        type_: NodeType,
        properties: Optional[NodeProperties] = None,
    ) -> None:
        """Create a new node. Nodes can be classes, packages, participants etc."""
        if properties is None:
            properties = NodeProperties(label=name)
        self.emit(f'{self._indent}node: {{title:"{name}"', force_newline=False)
        label = properties.label if properties.label is not None else name
        self._write_attributes(
            self.NODE_ATTRS,
            label=label,
            shape=self.SHAPES[type_],
        )
        self.emit("}")

    def emit_edge(
        self,
        from_node: str,
        to_node: str,
        type_: EdgeType,
        label: Optional[str] = None,
    ) -> None:
        """Create an edge from one node to another to display relationships."""
        self.emit(
            f'{self._indent}edge: {{sourcename:"{from_node}" targetname:"{to_node}"',
            force_newline=False,
        )
        attributes = self.ARROWS[type_]
        if label:
            attributes["label"] = label
        self._write_attributes(
            self.EDGE_ATTRS,
            **attributes,
        )
        self.emit("}")

    def _write_attributes(self, attributes_dict: Mapping[str, Any], **args) -> None:
        """write graph, node or edge attributes"""
        for key, value in args.items():
            try:
                _type = attributes_dict[key]
            except KeyError as e:
                raise Exception(
                    f"no such attribute {key}\npossible attributes are {attributes_dict.keys()}"
                ) from e

            if not _type:
                self.emit(f'{self._indent}{key}:"{value}"\n')
            elif _type == 1:
                self.emit(f"{self._indent}{key}:{int(value)}\n")
            elif value in _type:
                self.emit(f"{self._indent}{key}:{value}\n")
            else:
                raise Exception(
                    f"value {value} isn't correct for attribute {key} correct values are {type}"
                )

    def _close_graph(self) -> None:
        """Emit the lines needed to properly close the graph."""
        self._dec_indent()
        self.emit(f"{self._indent}}}")


class DotPrinter(Printer):
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
    RANKDIR: Dict[Layout, str] = {
        Layout.LEFT_TO_RIGHT: "LR",
        Layout.RIGHT_TO_LEFT: "RL",
        Layout.TOP_TO_BOTTOM: "TB",
        Layout.BOTTOM_TO_TOP: "BT",
    }

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
            self.emit(f"rankdir={self.RANKDIR[self.layout]}")
        if self.charset:
            assert (
                self.charset.lower() in self.ALLOWED_CHARSETS
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
        shape = self.SHAPES[type_]
        color = properties.color if properties.color is not None else "black"
        label = properties.label
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

    def emit_edge(
        self,
        from_node: str,
        to_node: str,
        type_: EdgeType,
        label: Optional[str] = None,
    ) -> None:
        """Create an edge from one node to another to display relationships."""
        arrowstyle = self.ARROWS[type_]
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
            target = get_file_extension(outputfile)
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
            if shutil.which("dot") is None:
                raise RuntimeError(
                    f"Cannot generate `{outputfile}` because 'dot' "
                    "executable not found. Install graphviz, or specify a `.gv` "
                    "outputfile to produce the DOT source code."
                )
            use_shell = sys.platform == "win32"
            subprocess.call(
                ["dot", "-T", target, dot_sourcepath, "-o", outputfile],
                shell=use_shell,
            )
            os.unlink(dot_sourcepath)
        # return outputfile  TODO should we return this?

    def _close_graph(self) -> None:
        """Emit the lines needed to properly close the graph."""
        self.emit("}\n")
