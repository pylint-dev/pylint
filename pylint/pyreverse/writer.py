# -*- coding: utf-8 -*-
# Copyright (c) 2008-2010, 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Mike Frysinger <vapier@gentoo.org>
# Copyright (c) 2015 Florian Bruhin <me@the-compiler.org>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2018 Anthony Sottile <asottile@umich.edu>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import os.path

"""Utilities for creating VCG and Dot diagrams"""

from pylint.graph import DotBackend
from pylint.pyreverse.utils import is_exception
from pylint.pyreverse.vcgutils import VCGPrinter


class DiagramWriter:
    """base class for writing project diagrams
    """

    def __init__(self, config, styles):
        self.config = config
        self.pkg_edges, self.inh_edges, self.imp_edges, self.association_edges = styles
        self.printer = None  # defined in set_printer

    def write(self, diadefs):
        """write files for <project> according to <diadefs>
        """
        for diagram in diadefs:
            basename = diagram.title.strip().replace(" ", "_")
            file_name = "%s.%s" % (basename, self.config.output_format)
            self.set_printer(file_name, basename)
            if diagram.TYPE == "class":
                self.write_classes(diagram)
            else:
                self.write_packages(diagram)
            self.close_graph()

    def write_packages(self, diagram):
        """write a package diagram"""
        # sorted to get predictable (hence testable) results
        for i, obj in enumerate(sorted(diagram.modules(), key=lambda x: x.title)):
            self.printer.emit_node(i, label=self.get_title(obj), shape="box")
            obj.fig_id = i
        # package dependencies
        for rel in diagram.get_relationships("depends"):
            self.printer.emit_edge(
                rel.from_object.fig_id, rel.to_object.fig_id, **self.pkg_edges
            )

    def write_classes(self, diagram):
        """write a class diagram"""
        # sorted to get predictable (hence testable) results
        for i, obj in enumerate(sorted(diagram.objects, key=lambda x: x.title)):
            self.printer.emit_node(i, **self.get_values(obj))
            obj.fig_id = i
        # inheritance links
        for rel in diagram.get_relationships("specialization"):
            self.printer.emit_edge(
                rel.from_object.fig_id, rel.to_object.fig_id, **self.inh_edges
            )
        # implementation links
        for rel in diagram.get_relationships("implements"):
            self.printer.emit_edge(
                rel.from_object.fig_id, rel.to_object.fig_id, **self.imp_edges
            )
        # generate associations
        for rel in diagram.get_relationships("association"):
            self.printer.emit_edge(
                rel.from_object.fig_id,
                rel.to_object.fig_id,
                label=rel.name,
                **self.association_edges
            )

    def set_printer(self, file_name, basename):
        """set printer"""
        raise NotImplementedError

    def get_title(self, obj):
        """get project title"""
        raise NotImplementedError

    def get_values(self, obj):
        """get label and shape for classes."""
        raise NotImplementedError

    def close_graph(self):
        """finalize the graph"""
        raise NotImplementedError


class DotWriter(DiagramWriter):
    """write dot graphs from a diagram definition and a project
    """

    def __init__(self, config):
        styles = [
            dict(arrowtail="none", arrowhead="open"),
            dict(arrowtail="none", arrowhead="empty"),
            dict(arrowtail="node", arrowhead="empty", style="dashed"),
            dict(
                fontcolor="green", arrowtail="none", arrowhead="diamond", style="solid"
            ),
        ]
        DiagramWriter.__init__(self, config, styles)

    def set_printer(self, file_name, basename):
        """initialize DotWriter and add options for layout.
        """
        layout = dict(rankdir="BT")
        self.printer = DotBackend(basename, additional_param=layout)
        self.file_name = file_name

    def get_title(self, obj):
        """get project title"""
        return obj.title

    def get_values(self, obj):
        """get label and shape for classes.

        The label contains all attributes and methods
        """
        label = obj.title
        if obj.shape == "interface":
            label = "«interface»\\n%s" % label
        if not self.config.only_classnames:
            label = r"%s|%s\l|" % (label, r"\l".join(obj.attrs))
            for func in obj.methods:
                if func.args.args:
                    args = [arg.name for arg in func.args.args if arg.name != "self"]
                else:
                    args = []
                label = r"%s%s(%s)\l" % (label, func.name, ", ".join(args))
            label = "{%s}" % label
        if is_exception(obj.node):
            return dict(fontcolor="red", label=label, shape="record")
        return dict(label=label, shape="record")

    def close_graph(self):
        """print the dot graph into <file_name>"""
        self.printer.generate(self.file_name)


class VCGWriter(DiagramWriter):
    """write vcg graphs from a diagram definition and a project
    """

    def __init__(self, config):
        styles = [
            dict(arrowstyle="solid", backarrowstyle="none", backarrowsize=0),
            dict(arrowstyle="solid", backarrowstyle="none", backarrowsize=10),
            dict(
                arrowstyle="solid",
                backarrowstyle="none",
                linestyle="dotted",
                backarrowsize=10,
            ),
            dict(arrowstyle="solid", backarrowstyle="none", textcolor="green"),
        ]
        DiagramWriter.__init__(self, config, styles)

    def set_printer(self, file_name, basename):
        """initialize VCGWriter for a UML graph"""
        self.graph_file = open(file_name, "w+")
        self.printer = VCGPrinter(self.graph_file)
        self.printer.open_graph(
            title=basename,
            layoutalgorithm="dfs",
            late_edge_labels="yes",
            port_sharing="no",
            manhattan_edges="yes",
        )
        self.printer.emit_node = self.printer.node
        self.printer.emit_edge = self.printer.edge

    def get_title(self, obj):
        """get project title in vcg format"""
        return r"\fb%s\fn" % obj.title

    def get_values(self, obj):
        """get label and shape for classes.

        The label contains all attributes and methods
        """
        if is_exception(obj.node):
            label = r"\fb\f09%s\fn" % obj.title
        else:
            label = r"\fb%s\fn" % obj.title
        if obj.shape == "interface":
            shape = "ellipse"
        else:
            shape = "box"
        if not self.config.only_classnames:
            attrs = obj.attrs
            methods = [func.name for func in obj.methods]
            # box width for UML like diagram
            maxlen = max(len(name) for name in [obj.title] + methods + attrs)
            line = "_" * (maxlen + 2)
            label = r"%s\n\f%s" % (label, line)
            for attr in attrs:
                label = r"%s\n\f08%s" % (label, attr)
            if attrs:
                label = r"%s\n\f%s" % (label, line)
            for func in methods:
                label = r"%s\n\f10%s()" % (label, func)
        return dict(label=label, shape=shape)

    def close_graph(self):
        """close graph and file"""
        self.printer.close_graph()
        self.graph_file.close()

class PlantUMLWriter(DiagramWriter):
    """base class for writing project diagrams
    """

    def __init__(self, config, styles):

        self.config = config
        self.pkg_edges, self.inh_edges, self.imp_edges, self.association_edges = styles
        self.printer = None  # defined in set_printer

        self.projectname = ""
        self.packagestate = ""
        self._stream = None
        self.classarr = []

    def write(self, diadefs):
        """write files for <project> according to <diadefs>
        """
        for diagram in diadefs:
            basename = diagram.title.strip().replace(" ", "_")
            file_name = "%s.%s" % (basename, self.config.output_format)
 
            self.set_printer(file_name, basename)
            if diagram.TYPE == "class":
                self.write_classes(diagram)
            else:
                self.write_packages(diagram)
            self.close_graph()

    def write_packages(self, diagram):
        """write a package diagram"""
        # sorted to get predictable (hence testable) results
        for i, obj in enumerate(sorted(diagram.modules(), key=lambda x: x.title)):
            pkg_name = self.get_title(obj)
            prefix = os.path.commonprefix([pkg_name, self.packagestate])
            if prefix == self.packagestate:
                self._stream.write("}\n")
                self.packagestate = pkg_name
            else:
                self._stream.write("}\n")
                for _ in range(self.packagestate.count(".", len(prefix))):
                    self._stream.write("}\n")
                if pkg_name != "":
                    self._stream.write("package %s { \n" % pkg_name)
                    self.packagestate = pkg_name

            obj.fig_id = i
        # package dependencies
        for rel in diagram.get_relationships("depends"):
            pass # NotImplemented

    def write_classes(self, diagram):
        """write a class diagram"""
        # sorted to get predictable (hence testable) results
        for i, obj in enumerate(sorted(diagram.objects, key=lambda x: x.title)):
            args = self.get_values(obj)
            if 'label' in args and 'classname' in args:
                self.classarr.append(args['classname'])
                assert self.classarr[i] == args['classname']
                self._stream.write("class %s { %s \n %s \n}\n" % (args['classname'], args['attributes'], args['methods']))
            obj.fig_id = i
        # inheritance links
        for rel in diagram.get_relationships("specialization"):
            # plantuml: --|>
            self._stream.write("%s --|> %s" % (rel.from_object.title, rel.to_object.title))
        # implementation links
        for rel in diagram.get_relationships("implements"):
            pass
        # generate associations
        for rel in diagram.get_relationships("association"):
            self._stream.write("%s -- %s" % (rel.from_object.title, rel.to_object.title))

    def set_printer(self, file_name, basename):
        """set printer"""
        self._stream = open(file_name, "w+")
        self._stream.write("@startuml\n")

    def get_title(self, obj):
        """get project title"""
        if "/" in obj.title:
            if not self.projectname:
                last = obj.title.rfind('/')
                prelast = obj.title.rfind('/',0,last)
                self.projectname = prelast
            else:
                prelast = self.projectname
            title = obj.title[prelast + 1:]
            title = title.replace("/__init__.py", '')
            title = title.replace(".py", '')
            title = title.replace("/", '.')

        else:
            title = obj.title
        return title

    def get_values(self, obj):
        """get label and shape for classes."""
        if is_exception(obj.node):
            print("Exception Warning")
        if obj.shape == "interface":
            shape = "ellipse"
        else:
            shape = "box"
        if not self.config.only_classnames:
            attrs = obj.attrs
            methods = [func.name for func in obj.methods]
            # box width for UML like diagram
            #maxlen = max(len(name) for name in [obj.title] + methods + attrs)
            #line = "_" * (maxlen + 2)
            label = ""
            for attr in attrs:
                label += "\n  %s" % (attr)
            if attrs:
                label += "\n"
            for func in methods:
                label += "\n  %s()" % (func)
        return {"classname" : self.get_title(obj),"label" : label, "shape" :  shape}

    def close_graph(self):
        """finalize the graph"""
        self._stream.write("@enduml")
        self._stream.close()
