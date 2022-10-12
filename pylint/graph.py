# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Graph manipulation utilities.

(dot generation adapted from pypy/translator/tool/make_dot.py)
"""

from __future__ import annotations

import codecs
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from typing import Any, Union


def target_info_from_filename(filename: str) -> tuple[str, str, str]:
    """Transforms /some/path/foo.png into ('/some/path', 'foo.png', 'png')."""
    basename = os.path.basename(filename)
    storedir = os.path.dirname(os.path.abspath(filename))
    target = os.path.splitext(filename)[-1][1:]
    return storedir, basename, target


class DotBackend:
    """Dot File back-end."""

    def __init__(
        self,
        graphname: str,
        rankdir: str | None = None,
        size: Any = None,
        ratio: Any = None,
        charset: str = "utf-8",
        renderer: str = "dot",
        additional_param: dict[str, Any] | None = None,
    ) -> None:
        if additional_param is None:
            additional_param = {}
        self.graphname = graphname
        self.renderer = renderer
        self.lines: list[str] = []
        self._source: str | None = None
        self.emit(f"digraph {normalize_node_id(graphname)} {{")
        if rankdir:
            self.emit(f"rankdir={rankdir}")
        if ratio:
            self.emit(f"ratio={ratio}")
        if size:
            self.emit(f'size="{size}"')
        if charset:
            assert charset.lower() in {
                "utf-8",
                "iso-8859-1",
                "latin1",
            }, f"unsupported charset {charset}"
            self.emit(f'charset="{charset}"')
        for param in additional_param.items():
            self.emit("=".join(param))

    def get_source(self) -> str:
        """Returns self._source."""
        if self._source is None:
            self.emit("}\n")
            self._source = "\n".join(self.lines)
            del self.lines
        return self._source

    source = property(get_source)

    def generate(
        self, outputfile: str | None = None, mapfile: str | None = None
    ) -> str:
        """Generates a graph file.

        :param str outputfile: filename and path [defaults to graphname.png]
        :param str mapfile: filename and path

        :rtype: str
        :return: a path to the generated file
        :raises RuntimeError: if the executable for rendering was not found
        """
        # pylint: disable=duplicate-code
        graphviz_extensions = ("dot", "gv")
        name = self.graphname
        if outputfile is None:
            target = "png"
            pdot, dot_sourcepath = tempfile.mkstemp(".gv", name)
            ppng, outputfile = tempfile.mkstemp(".png", name)
            os.close(pdot)
            os.close(ppng)
        else:
            _, _, target = target_info_from_filename(outputfile)
            if not target:
                target = "png"
                outputfile = outputfile + "." + target
            if target not in graphviz_extensions:
                pdot, dot_sourcepath = tempfile.mkstemp(".gv", name)
                os.close(pdot)
            else:
                dot_sourcepath = outputfile
        with codecs.open(dot_sourcepath, "w", encoding="utf8") as file:
            file.write(self.source)
        if target not in graphviz_extensions:
            if shutil.which(self.renderer) is None:
                raise RuntimeError(
                    f"Cannot generate `{outputfile}` because '{self.renderer}' "
                    "executable not found. Install graphviz, or specify a `.gv` "
                    "outputfile to produce the DOT source code."
                )
            use_shell = sys.platform == "win32"
            if mapfile:
                subprocess.call(
                    [
                        self.renderer,
                        "-Tcmapx",
                        "-o",
                        mapfile,
                        "-T",
                        target,
                        dot_sourcepath,
                        "-o",
                        outputfile,
                    ],
                    shell=use_shell,
                )
            else:
                subprocess.call(
                    [self.renderer, "-T", target, dot_sourcepath, "-o", outputfile],
                    shell=use_shell,
                )
            os.unlink(dot_sourcepath)
        return outputfile

    def emit(self, line: str) -> None:
        """Adds <line> to final output."""
        self.lines.append(line)

    def emit_edge(self, name1: str, name2: str, **props: Any) -> None:
        """Emit an edge from <name1> to <name2>.

        For edge properties: see https://www.graphviz.org/doc/info/attrs.html
        """
        attrs = [f'{prop}="{value}"' for prop, value in props.items()]
        n_from, n_to = normalize_node_id(name1), normalize_node_id(name2)
        self.emit(f"{n_from} -> {n_to} [{', '.join(sorted(attrs))}];")

    def emit_node(self, name: str, **props: Any) -> None:
        """Emit a node with given properties.

        For node properties: see https://www.graphviz.org/doc/info/attrs.html
        """
        attrs = [f'{prop}="{value}"' for prop, value in props.items()]
        self.emit(f"{normalize_node_id(name)} [{', '.join(sorted(attrs))}];")


def normalize_node_id(nid: str) -> str:
    """Returns a suitable DOT node id for `nid`."""
    return f'"{nid}"'


def get_cycles(
    graph_dict: dict[str, set[str]], vertices: list[str] | None = None
) -> Sequence[list[str]]:
    """Return a list of detected cycles based on an ordered graph (i.e. keys are
    vertices and values are lists of destination vertices representing edges).
    """
    if not graph_dict:
        return ()
    result: list[list[str]] = []
    if vertices is None:
        vertices = list(graph_dict.keys())
    for vertice in vertices:
        _get_cycles(graph_dict, [], set(), result, vertice)
    return result


def _get_cycles(
    graph_dict: dict[str, set[str]],
    path: list[str],
    visited: set[str],
    result: list[list[str]],
    vertice: str,
) -> None:
    """Recursive function doing the real work for get_cycles."""
    if vertice in path:
        cycle = [vertice]
        for node in path[::-1]:
            if node == vertice:
                break
            cycle.insert(0, str(node))
        # make a canonical representation
        start_from = min(cycle)
        index = cycle.index(start_from)
        cycle = cycle[index:] + cycle[0:index]
        # append it to result if not already in
        if cycle not in result:
            result.append(cycle)
        return
    path.append(vertice)
    try:
        for node in graph_dict[vertice]:
            # don't check already visited nodes again
            if node not in visited:
                _get_cycles(graph_dict, path, visited, result, node)
                visited.add(node)
    except KeyError:
        pass
    path.pop()


node_types = Union[str, int, float]


def get_paths(
    graph_dict: dict[node_types, set[node_types]],
    indegree_dict: dict[node_types, int],
    frequency_dict: dict[tuple[node_types, node_types], int],
) -> list[tuple[node_types]]:
    """Gets the minimum number of paths that span all the edges in graph_dict."""
    to_visit = {node for node in indegree_dict if indegree_dict[node] == 0}
    paths = set()
    while to_visit:
        symbols_in_longest_path: dict[node_types, int] = {}
        nodes_in_longest_path: dict[node_types, int] = {}

        # Count the longest possible paths rooted at each node
        for root in to_visit:
            count_nodes(
                root,
                graph_dict,
                symbols_in_longest_path,
                nodes_in_longest_path,
                frequency_dict,
            )
        path: list[node_types] = []

        # Get the node that can give us the longest path
        longest_path_item = get_longest_path_item(
            to_visit, symbols_in_longest_path, nodes_in_longest_path
        )
        to_visit.remove(longest_path_item)
        get_path(
            path,
            graph_dict,
            longest_path_item,
            to_visit,
            frequency_dict,
            symbols_in_longest_path,
            nodes_in_longest_path,
        )

        # Decrement the times we can use each node we visited so they are not revisited
        for i, item in enumerate(path):
            for val in path[:i]:
                frequency_dict[(val, item)] = max(frequency_dict[(val, item)] - 1, 0)

        path = strip_path(path)
        if len(path) > 1:
            paths.add(tuple(path))

    return sorted(list(paths), key=str)  # type: ignore[arg-type]


def get_longest_path_item(
    items: set[node_types],
    symbols_in_longest_path: dict[node_types, int],
    nodes_in_longest_path: dict[node_types, int],
) -> node_types:
    """Return the item that is at the root of the longest path, prioritizing the number
    of symbols (a, b, c) and breaking ties with the total number of nodes in the path.

    and then the node value alphabetically.
    """
    return sorted(
        items,
        reverse=True,
        key=lambda x: (symbols_in_longest_path[x], nodes_in_longest_path[x], str(x)),
    )[0]


def get_path(
    path: list[node_types],
    graph_dict: dict[node_types, set[node_types]],
    node: node_types,
    to_visit: set[node_types],
    frequency_dict: dict[tuple[node_types, node_types], int],
    symbols_in_longest_path: dict[node_types, int],
    nodes_in_longest_path: dict[node_types, int],
) -> None:
    """Appends to path the longest possible path in graph_dict starting at node."""
    path.append(node)
    # Find viable neighbors that can be in the path
    adj = {a for a in graph_dict[node] if frequency_dict[(node, a)] != 0}
    if len(adj) >= 1:
        # Select the neighbor that will yield the longest path
        next_item = get_longest_path_item(
            adj, symbols_in_longest_path, nodes_in_longest_path
        )
        # Recursively get the path through that neighbor
        get_path(
            path,
            graph_dict,
            next_item,
            to_visit,
            frequency_dict,
            symbols_in_longest_path,
            nodes_in_longest_path,
        )

        # If there are other adjacent nodes, or this node has more paths going through it, we need to revisit it
        if len(adj) >= 2 or frequency_dict[(node, next_item)] >= 2:
            to_visit.add(node)


def count_nodes(
    node: node_types,
    graph_dict: dict[node_types, set[node_types]],
    symbols_in_longest_path: dict[node_types, int],
    nodes_in_longest_path: dict[node_types, int],
    frequency_dict: dict[tuple[node_types, node_types], int],
) -> tuple[int, int]:
    """Calculates the number of symbols and nodes in the longest path reachable from
    node and stores them in symbols_in_longest_path and nodes_in_longest_path.
    """
    # Already calculated
    if node in symbols_in_longest_path and node in nodes_in_longest_path:
        return (symbols_in_longest_path[node], nodes_in_longest_path[node])

    adj = [a for a in graph_dict[node] if frequency_dict[(node, a)] != 0]
    cur_node_symbol_count = (
        1 if isinstance(node, str) else 0
    )  # Indicates if the current node is a symbol
    if not adj:  # Base case if there are no neighbors
        max_symbols_path = cur_node_symbol_count
        max_nodes_path = 1
    else:  # Calculate the paths recursively based on the maximum lengths of neighbor nodes
        adj_maximums = [
            count_nodes(
                a,
                graph_dict,
                symbols_in_longest_path,
                nodes_in_longest_path,
                frequency_dict,
            )
            for a in adj
        ]
        max_symbols_path = (
            max(adj_maxes[0] for adj_maxes in adj_maximums) + cur_node_symbol_count
        )
        max_nodes_path = max(adj_maxes[1] for adj_maxes in adj_maximums) + 1

    # Update the graph and return
    symbols_in_longest_path[node] = max_symbols_path
    nodes_in_longest_path[node] = max_nodes_path
    return (max_symbols_path, max_nodes_path)


def strip_path(path: list[node_types]) -> list[node_types]:
    """Removes redundant constant comparisons at the ends of a path, e.g. simplies {a,
    3, 0} to {a, 3}.
    """
    low = 0
    high = len(path) - 1
    if path and isinstance(path[0], (int, float)):
        while (
            low < len(path) - 1
            and isinstance(path[low], (int, float))
            and isinstance(path[low + 1], (int, float))
        ):
            low += 1

    if path and isinstance(path[-1], (int, float)):
        while (
            high > 0
            and high > low
            and isinstance(path[high], (int, float))
            and isinstance(path[high - 1], (int, float))
        ):
            high -= 1
    return path[low : high + 1]
