# Copyright (c) 2008-2010, 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Mike Frysinger <vapier@gentoo.org>
# Copyright (c) 2015 Florian Bruhin <me@the-compiler.org>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2018, 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Kylian <development@goudcode.nl>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>
# Copyright (c) 2021 Mark Byrne <31762852+mbyrnepr2@users.noreply.github.com>
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Utilities for creating VCG and Dot diagrams"""

import os

from pylint.pyreverse.diagrams import (
    ClassDiagram,
    ClassEntity,
    PackageDiagram,
    PackageEntity,
)
from pylint.pyreverse.printer import EdgeType, NodeProperties, NodeType
from pylint.pyreverse.printer_factory import get_printer_for_filetype
from pylint.pyreverse.utils import is_exception


class DiagramWriter:
    """base class for writing project diagrams"""

    def __init__(self, config):
        self.config = config
        self.printer_class = get_printer_for_filetype(self.config.output_format)
        self.printer = None  # defined in set_printer
        self.file_name = ""  # defined in set_printer

    def write(self, diadefs):
        """write files for <project> according to <diadefs>"""
        for diagram in diadefs:
            basename = diagram.title.strip().replace(" ", "_")
            file_name = f"{basename}.{self.config.output_format}"
            if os.path.exists(self.config.output_directory):
                file_name = os.path.join(self.config.output_directory, file_name)
            self.set_printer(file_name, basename)
            if diagram.TYPE == "class":
                self.write_classes(diagram)
            else:
                self.write_packages(diagram)
            self.save()

    def write_packages(self, diagram: PackageDiagram) -> None:
        """write a package diagram"""
        # sorted to get predictable (hence testable) results
        for module in sorted(diagram.modules(), key=lambda x: x.title):
            module.fig_id = module.node.qname()
            self.printer.emit_node(
                module.fig_id,
                type_=NodeType.PACKAGE,
                properties=self.get_package_properties(module),
            )
        # package dependencies
        for rel in diagram.get_relationships("depends"):
            self.printer.emit_edge(
                rel.from_object.fig_id,
                rel.to_object.fig_id,
                type_=EdgeType.USES,
            )

    def write_classes(self, diagram: ClassDiagram) -> None:
        """write a class diagram"""
        # sorted to get predictable (hence testable) results
        for obj in sorted(diagram.objects, key=lambda x: x.title):
            obj.fig_id = obj.node.qname()
            type_ = NodeType.INTERFACE if obj.shape == "interface" else NodeType.CLASS
            self.printer.emit_node(
                obj.fig_id, type_=type_, properties=self.get_class_properties(obj)
            )
        # inheritance links
        for rel in diagram.get_relationships("specialization"):
            self.printer.emit_edge(
                rel.from_object.fig_id,
                rel.to_object.fig_id,
                type_=EdgeType.INHERITS,
            )
        # implementation links
        for rel in diagram.get_relationships("implements"):
            self.printer.emit_edge(
                rel.from_object.fig_id,
                rel.to_object.fig_id,
                type_=EdgeType.IMPLEMENTS,
            )
        # generate associations
        for rel in diagram.get_relationships("association"):
            self.printer.emit_edge(
                rel.from_object.fig_id,
                rel.to_object.fig_id,
                label=rel.name,
                type_=EdgeType.ASSOCIATION,
            )

    def set_printer(self, file_name: str, basename: str) -> None:
        """set printer"""
        self.printer = self.printer_class(basename)
        self.file_name = file_name

    @staticmethod
    def get_package_properties(obj: PackageEntity) -> NodeProperties:
        """get label and shape for packages."""
        return NodeProperties(
            label=obj.title,
            color="black",
        )

    def get_class_properties(self, obj: ClassEntity) -> NodeProperties:
        """get label and shape for classes."""
        properties = NodeProperties(
            label=obj.title,
            attrs=obj.attrs if not self.config.only_classnames else None,
            methods=obj.methods if not self.config.only_classnames else None,
            fontcolor="red" if is_exception(obj.node) else "black",
            color="black",
        )
        return properties

    def save(self) -> None:
        """write to disk"""
        self.printer.generate(self.file_name)
