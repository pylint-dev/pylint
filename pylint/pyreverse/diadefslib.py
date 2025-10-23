# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Handle diagram generation options for class diagram or default diagrams."""

from __future__ import annotations

import argparse
import warnings
from collections import defaultdict
from collections.abc import Generator, Sequence
from typing import Any

import astroid
from astroid import nodes
from astroid.modutils import is_stdlib_module

from pylint.pyreverse.diagrams import ClassDiagram, PackageDiagram, Relationship
from pylint.pyreverse.inspector import Linker, Project
from pylint.pyreverse.utils import LocalsVisitor

# diagram generators ##########################################################


class DiaDefGenerator:
    """Handle diagram generation options."""

    def __init__(self, linker: Linker, handler: DiadefsHandler) -> None:
        """Common Diagram Handler initialization."""
        self.config = handler.config
        self.args = handler.args
        self.module_names: bool = False
        self._set_default_options()
        self.linker = linker
        self.classdiagram: ClassDiagram  # defined by subclasses
        # Only pre-calculate depths if user has requested a max_depth
        if handler.config.max_depth is not None:
            # Detect which of the args are leaf nodes
            leaf_nodes = self.get_leaf_nodes()

            # Emit a warning if any of the args are not leaf nodes
            diff = set(self.args).difference(set(leaf_nodes))
            if len(diff) > 0:
                warnings.warn(
                    "Detected nested names within the specified packages. "
                    f"The following packages: {sorted(diff)} will be ignored for "
                    f"depth calculations, using only: {sorted(leaf_nodes)} as the base for limiting "
                    "package depth.",
                    stacklevel=2,
                )

            self.args_depths = {module: module.count(".") for module in leaf_nodes}

    def get_title(self, node: nodes.ClassDef) -> str:
        """Get title for objects."""
        title = node.name
        if self.module_names:
            title = f"{node.root().name}.{title}"
        return title  # type: ignore[no-any-return]

    def get_leaf_nodes(self) -> list[str]:
        """
        Get the leaf nodes from the list of args in the generator.

        A leaf node is one that is not a prefix (with an extra dot) of any other node.
        """
        leaf_nodes = [
            module
            for module in self.args
            if not any(
                other != module and other.startswith(module + ".")
                for other in self.args
            )
        ]
        return leaf_nodes

    def _set_option(self, option: bool | None) -> bool:
        """Activate some options if not explicitly deactivated."""
        # if we have a class diagram, we want more information by default;
        # so if the option is None, we return True
        if option is None:
            return bool(self.config.classes)
        return option

    def _set_default_options(self) -> None:
        """Set different default options with _default dictionary."""
        self.module_names = self._set_option(self.config.module_names)
        all_ancestors = self._set_option(self.config.all_ancestors)
        all_associated = self._set_option(self.config.all_associated)
        anc_level, association_level = (0, 0)
        if all_ancestors:
            anc_level = -1
        if all_associated:
            association_level = -1
        if self.config.show_ancestors is not None:
            anc_level = self.config.show_ancestors
        if self.config.show_associated is not None:
            association_level = self.config.show_associated
        self.anc_level, self.association_level = anc_level, association_level

    def _get_levels(self) -> tuple[int, int]:
        """Help function for search levels."""
        return self.anc_level, self.association_level

    def _should_include_by_depth(self, node: nodes.NodeNG) -> bool:
        """Check if a node should be included based on depth.

        A node will be included if it is at or below the max_depth relative to the
        specified base packages. A node is considered to be a base package if it is the
        deepest package in the list of specified packages. In other words the base nodes
        are the leaf nodes of the specified package tree.
        """
        # If max_depth is not set, include all nodes
        if self.config.max_depth is None:
            return True

        # Calculate the absolute depth of the node
        name = node.root().name
        absolute_depth = name.count(".")

        # Retrieve the base depth to compare against
        relative_depth = next(
            (v for k, v in self.args_depths.items() if name.startswith(k)), None
        )
        return relative_depth is not None and bool(
            (absolute_depth - relative_depth) <= self.config.max_depth
        )

    def show_node(self, node: nodes.ClassDef) -> bool:
        """Determine if node should be shown based on config."""
        if node.root().name == "builtins":
            return self.config.show_builtin  # type: ignore[no-any-return]

        if is_stdlib_module(node.root().name):
            return self.config.show_stdlib  # type: ignore[no-any-return]

        # Filter node by depth
        return self._should_include_by_depth(node)

    def add_class(self, node: nodes.ClassDef) -> None:
        """Visit one class and add it to diagram."""
        self.linker.visit(node)
        self.classdiagram.add_object(self.get_title(node), node)

    def get_ancestors(
        self, node: nodes.ClassDef, level: int
    ) -> Generator[nodes.ClassDef]:
        """Return ancestor nodes of a class node."""
        if level == 0:
            return
        for ancestor in node.ancestors(recurs=False):
            if not self.show_node(ancestor):
                continue
            yield ancestor

    def get_associated(
        self, klass_node: nodes.ClassDef, level: int
    ) -> Generator[nodes.ClassDef]:
        """Return associated nodes of a class node."""
        if level == 0:
            return
        for association_nodes in list(klass_node.instance_attrs_type.values()) + list(
            klass_node.locals_type.values()
        ):
            for node in association_nodes:
                if isinstance(node, astroid.Instance):
                    node = node._proxied
                if not (isinstance(node, nodes.ClassDef) and self.show_node(node)):
                    continue
                yield node

    def extract_classes(
        self, klass_node: nodes.ClassDef, anc_level: int, association_level: int
    ) -> None:
        """Extract recursively classes related to klass_node."""
        if self.classdiagram.has_node(klass_node) or not self.show_node(klass_node):
            return
        self.add_class(klass_node)

        for ancestor in self.get_ancestors(klass_node, anc_level):
            self.extract_classes(ancestor, anc_level - 1, association_level)

        for node in self.get_associated(klass_node, association_level):
            self.extract_classes(node, anc_level, association_level - 1)


class DefaultDiadefGenerator(LocalsVisitor, DiaDefGenerator):
    """Generate minimum diagram definition for the project :

    * a package diagram including project's modules
    * a class diagram including project's classes
    """

    def __init__(self, linker: Linker, handler: DiadefsHandler) -> None:
        DiaDefGenerator.__init__(self, linker, handler)
        LocalsVisitor.__init__(self)

    def visit_project(self, node: Project) -> None:
        """Visit a pyreverse.utils.Project node.

        create a diagram definition for packages
        """
        mode = self.config.mode
        if len(node.modules) > 1:
            self.pkgdiagram: PackageDiagram | None = PackageDiagram(
                f"packages {node.name}", mode
            )
        else:
            self.pkgdiagram = None
        self.classdiagram = ClassDiagram(f"classes {node.name}", mode)

    def leave_project(self, _: Project) -> Any:
        """Leave the pyreverse.utils.Project node.

        return the generated diagram definition
        """
        if self.pkgdiagram:
            return self.pkgdiagram, self.classdiagram
        return (self.classdiagram,)

    def visit_module(self, node: nodes.Module) -> None:
        """Visit an nodes.Module node.

        add this class to the package diagram definition
        """
        if self.pkgdiagram and self._should_include_by_depth(node):
            self.linker.visit(node)
            self.pkgdiagram.add_object(node.name, node)

    def visit_classdef(self, node: nodes.ClassDef) -> None:
        """Visit an nodes.Class node.

        add this class to the class diagram definition
        """
        anc_level, association_level = self._get_levels()
        self.extract_classes(node, anc_level, association_level)

    def visit_importfrom(self, node: nodes.ImportFrom) -> None:
        """Visit nodes.ImportFrom  and catch modules for package diagram."""
        if self.pkgdiagram and self._should_include_by_depth(node):
            self.pkgdiagram.add_from_depend(node, node.modname)


class ClassDiadefGenerator(DiaDefGenerator):
    """Generate a class diagram definition including all classes related to a
    given class.
    """

    def class_diagram(self, project: Project, klass: nodes.ClassDef) -> ClassDiagram:
        """Return a class diagram definition for the class and related classes."""
        self.classdiagram = ClassDiagram(klass, self.config.mode)
        if len(project.modules) > 1:
            module, klass = klass.rsplit(".", 1)
            module = project.get_module(module)
        else:
            module = project.modules[0]
            klass = klass.split(".")[-1]
        klass = next(module.ilookup(klass))

        anc_level, association_level = self._get_levels()
        self.extract_classes(klass, anc_level, association_level)
        return self.classdiagram


# diagram handler #############################################################


class DiadefsHandler:
    """Get diagram definitions from user (i.e. xml files) or generate them."""

    def __init__(self, config: argparse.Namespace, args: Sequence[str]) -> None:
        self.config = config
        self.args = args

    def _get_object_name(self, obj: Any) -> str:
        """Get object name safely handling both title attributes and strings.

        :param obj: Object to get name from
        :return: Object name/title
        :rtype: str
        """
        return obj.title if hasattr(obj, "title") else str(obj)

    def _process_relationship(
        self, relationship: Relationship, unique_classes: dict[str, Any], obj: Any
    ) -> None:
        """Process a single relationship for deduplication.

        :param relationship: Relationship to process
        :param unique_classes: Dict of unique classes
        :param obj: Current object being processed
        """
        if relationship.from_object == obj:
            relationship.from_object = unique_classes[obj.node.qname()]
        if relationship.to_object == obj:
            relationship.to_object = unique_classes[obj.node.qname()]

    def _process_class_relationships(
        self, diagram: ClassDiagram, obj: Any, unique_classes: dict[str, Any]
    ) -> None:
        """Merge relationships for a class.

        :param diagram: Current diagram
        :param obj: Object whose relationships to process
        :param unique_classes: Dict of unique classes
        """
        for rel_type in ("specialization", "association", "aggregation"):
            for rel in diagram.get_relationships(rel_type):
                self._process_relationship(rel, unique_classes, obj)

    def deduplicate_classes(self, diagrams: list[ClassDiagram]) -> list[ClassDiagram]:
        """Remove duplicate classes from diagrams."""
        for diagram in diagrams:
            # Track unique classes by qualified name
            unique_classes: dict[str, Any] = {}
            duplicate_classes: Any = set()

            # First pass - identify duplicates
            for obj in diagram.objects:
                qname = obj.node.qname()
                if qname in unique_classes:
                    duplicate_classes.add(obj)
                    self._process_class_relationships(diagram, obj, unique_classes)
                else:
                    unique_classes[qname] = obj

            # Second pass - filter out duplicates
            diagram.objects = [
                obj for obj in diagram.objects if obj not in duplicate_classes
            ]

        return diagrams

    def _process_relationship_type(
        self,
        rel_list: list[Relationship],
        seen: set[tuple[str, str, str, Any | None]],
        unique_rels: dict[str, list[Relationship]],
        rel_name: str,
    ) -> None:
        """Process a list of relationships of a single type.

        :param rel_list: List of relationships to process
        :param seen: Set of seen relationships
        :param unique_rels: Dict to store unique relationships
        :param rel_name: Name of relationship type
        """
        for rel in rel_list:
            key = (
                self._get_object_name(rel.from_object),
                self._get_object_name(rel.to_object),
                type(rel).__name__,
                getattr(rel, "name", None),
            )
            if key not in seen:
                seen.add(key)
                unique_rels[rel_name].append(rel)

    def deduplicate_relationships(self, diagram: ClassDiagram) -> None:
        """Remove duplicate relationships between objects."""
        seen: set[tuple[str, str, str, Any | None]] = set()
        unique_rels: dict[str, list[Relationship]] = defaultdict(list)
        for rel_name, rel_list in diagram.relationships.items():
            self._process_relationship_type(rel_list, seen, unique_rels, rel_name)

        diagram.relationships = dict(unique_rels)

    def get_diadefs(self, project: Project, linker: Linker) -> list[ClassDiagram]:
        """Get the diagram's configuration data.

        :param project:The pyreverse project
        :type project: pyreverse.utils.Project
        :param linker: The linker
        :type linker: pyreverse.inspector.Linker(IdGeneratorMixIn, LocalsVisitor)

        :returns: The list of diagram definitions
        :rtype: list(:class:`pylint.pyreverse.diagrams.ClassDiagram`)
        """
        #  read and interpret diagram definitions (Diadefs)
        diagrams = []
        generator = ClassDiadefGenerator(linker, self)
        for klass in self.config.classes:
            diagrams.append(generator.class_diagram(project, klass))
        if not diagrams:
            diagrams = DefaultDiadefGenerator(linker, self).visit(project)
        for diagram in diagrams:
            diagram.extract_relationships()
            self.deduplicate_relationships(diagram)
        return self.deduplicate_classes(diagrams)
