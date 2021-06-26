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
# Copyright (c) 2021 Andreas Finkler <andi.finkler@gmail.com>
# Copyright (c) 2021 Mark Byrne <mbyrnepr2@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

"""Utilities for creating VCG and Dot diagrams"""

import itertools
import os
from typing import Type

import astroid
from astroid import modutils

from pylint.pyreverse.diagrams import (
    ClassDiagram,
    ClassEntity,
    DiagramEntity,
    PackageDiagram,
    PackageEntity,
)
from pylint.pyreverse.printer import (
    DotPrinter,
    EdgeType,
    Layout,
    NodeProperties,
    NodeType,
    PlantUmlPrinter,
    VCGPrinter,
)
from pylint.pyreverse.utils import (
    get_annotation_label,
    get_file_extension,
    is_exception,
)


class DiagramWriter:
    """base class for writing project diagrams"""

    def __init__(self, config):
        self.config = config
        self.printer = None  # defined in set_printer

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
        for obj in sorted(diagram.modules(), key=lambda x: x.title):
            obj.fig_id = obj.node.qname()
            self.printer.emit_node(
                obj.fig_id,
                type_=NodeType.PACKAGE,
                properties=self.get_package_properties(obj),
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
        raise NotImplementedError

    def get_title(self, obj: DiagramEntity) -> str:
        """get project title"""
        raise NotImplementedError

    def get_package_properties(self, obj: PackageEntity) -> NodeProperties:
        """get label and shape for packages."""
        raise NotImplementedError

    def get_class_properties(self, obj: ClassEntity) -> NodeProperties:
        """get label and shape for classes."""
        raise NotImplementedError

    def save(self) -> None:
        """write to disk"""
        raise NotImplementedError


class ColorMixin:
    """provide methods to apply colors to objects"""

    def __init__(self, depth):
        self.depth = depth
        self.available_colors = itertools.cycle(
            [
                "aliceblue",
                "antiquewhite",
                "aquamarine",
                "burlywood",
                "cadetblue",
                "chartreuse",
                "chocolate",
                "coral",
                "cornflowerblue",
                "cyan",
                "darkgoldenrod",
                "darkseagreen",
                "dodgerblue",
                "forestgreen",
                "gold",
                "hotpink",
                "mediumspringgreen",
            ]
        )
        self.used_colors = {}

    def get_color(self, obj: DiagramEntity) -> str:
        """get shape color"""
        qualified_name = obj.node.qname()
        if modutils.is_standard_module(qualified_name.split(".", maxsplit=1)[0]):
            return "grey"
        if isinstance(obj.node, astroid.ClassDef):
            package = qualified_name.rsplit(".", maxsplit=2)[0]
        elif obj.node.package:
            package = qualified_name
        else:
            package = qualified_name.rsplit(".", maxsplit=1)[0]
        base_name = ".".join(package.split(".", self.depth)[: self.depth])
        if base_name not in self.used_colors:
            self.used_colors[base_name] = next(self.available_colors)
        return self.used_colors[base_name]


class DotWriter(DiagramWriter, ColorMixin):
    """write dot graphs from a diagram definition and a project"""

    def __init__(self, config):
        DiagramWriter.__init__(self, config)
        ColorMixin.__init__(self, self.config.max_color_depth)

    def set_printer(self, file_name: str, basename: str) -> None:
        """initialize DotWriter and add options for layout."""
        self.printer = DotPrinter(
            basename, layout=Layout.BOTTOM_TO_TOP, colorized=self.config.colorized
        )
        self.file_name = file_name

    def get_title(self, obj: DiagramEntity) -> str:
        """get project title"""
        return obj.title

    def get_style(self) -> str:
        """get style of object"""
        if not self.config.colorized:
            return "solid"
        return "filled"

    def get_package_properties(self, obj: PackageEntity) -> NodeProperties:
        """get label and shape for packages."""
        return NodeProperties(
            label=self.get_title(obj),
            color=self.get_color(obj) if self.config.colorized else "black",
        )

    def get_class_properties(self, obj: ClassEntity) -> NodeProperties:
        """get label and shape for classes.

        The label contains all attributes and methods
        """
        label = obj.title
        if not self.config.only_classnames:
            label = r"{}|{}\l|".format(label, r"\l".join(obj.attrs))
            for func in obj.methods:
                return_type = (
                    f": {get_annotation_label(func.returns)}" if func.returns else ""
                )

                if func.args.args:
                    argument_list = [
                        arg for arg in func.args.args if arg.name != "self"
                    ]
                else:
                    argument_list = []

                annotations = dict(zip(argument_list, func.args.annotations[1:]))
                for arg in argument_list:
                    annotation_label = ""
                    ann = annotations.get(arg)
                    if ann:
                        annotation_label = get_annotation_label(ann)
                    annotations[arg] = annotation_label

                args = ", ".join(
                    f"{arg.name}: {ann}" if ann else f"{arg.name}"
                    for arg, ann in annotations.items()
                )

                label = fr"{label}{func.name}({args}){return_type}\l"
            label = "{%s}" % label
        properties = NodeProperties(
            label=label,
            fontcolor="red" if is_exception(obj.node) else "black",
            color=self.get_color(obj) if self.config.colorized else "black",
        )
        return properties

    def save(self) -> None:
        """write to disk"""
        self.printer.generate(self.file_name)


class VCGWriter(DiagramWriter):
    """write vcg graphs from a diagram definition and a project"""

    def set_printer(self, file_name: str, basename: str) -> None:
        """initialize VCGWriter for a UML graph"""
        self.file_name = file_name
        self.printer = VCGPrinter(basename)

    def get_title(self, obj: DiagramEntity) -> str:
        """get project title in vcg format"""
        return r"\fb%s\fn" % obj.title

    def get_package_properties(self, obj: PackageEntity) -> NodeProperties:
        """get label and shape for packages."""
        return NodeProperties(
            label=self.get_title(obj),
        )

    def get_class_properties(self, obj: ClassEntity) -> NodeProperties:
        """get label and shape for classes.

        The label contains all attributes and methods
        """
        if is_exception(obj.node):
            label = r"\fb\f09%s\fn" % obj.title
        else:
            label = r"\fb%s\fn" % obj.title
        if not self.config.only_classnames:
            attrs = obj.attrs
            methods = [func.name for func in obj.methods]
            # box width for UML like diagram
            maxlen = max(len(name) for name in [obj.title] + methods + attrs)
            line = "_" * (maxlen + 2)
            label = fr"{label}\n\f{line}"
            for attr in attrs:
                label = fr"{label}\n\f08{attr}"
            if attrs:
                label = fr"{label}\n\f{line}"
            for func in methods:
                label = fr"{label}\n\f10{func}()"
        return NodeProperties(label=label)

    def save(self) -> None:
        """write to disk"""
        self.printer.generate(self.file_name)


class PlantUmlWriter(DiagramWriter, ColorMixin):
    """write PlantUML graphs from a diagram definition and a project"""

    def __init__(self, config):
        self.file_name = None
        DiagramWriter.__init__(self, config)
        ColorMixin.__init__(self, self.config.max_color_depth)

    def set_printer(self, file_name: str, basename: str) -> None:
        """set printer"""
        self.file_name = file_name
        self.printer = PlantUmlPrinter(basename)

    def get_title(self, obj: DiagramEntity) -> str:
        """get project title"""
        return obj.title

    def get_package_properties(self, obj: PackageEntity) -> NodeProperties:
        """get label and shape for packages."""
        return NodeProperties(
            label=obj.title,
            color=self.get_color(obj) if self.config.colorized else None,
        )

    def get_class_properties(self, obj: ClassEntity) -> NodeProperties:
        """get label and shape for classes."""
        body = ""
        if not self.config.only_classnames:
            items = obj.attrs[:]
            for func in obj.methods:
                if func.args.args:
                    args = [arg.name for arg in func.args.args if arg.name != "self"]
                else:
                    args = []
                items.append(f'{func.name}({", ".join(args)})')
            body = "\n".join(items)
        return NodeProperties(
            label=obj.title,
            body=body,
            color=self.get_color(obj) if self.config.colorized else None,
        )

    def save(self) -> None:
        """write to disk"""
        self.printer.generate(self.file_name)


def get_writer_for_filetype(filename_or_extension: str) -> Type[DiagramWriter]:
    extension = get_file_extension(filename_or_extension)
    printer_mapping = {
        "dot": DotWriter,
        "vcg": VCGWriter,
        "puml": PlantUmlWriter,
    }
    return printer_mapping.get(extension, DotWriter)
