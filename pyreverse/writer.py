# -*- coding: utf-8 -*-
# Copyright (c) 2008 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
Utilities for VCG diagram output.
"""

from logilab.common.vcgutils import VCGPrinter
from logilab.common.graph import DotBackend

from pyreverse.utils import is_exception

class DiagramWriter:
    """base class for writing project diagrams
    """
    def __init__(self, config):
        self.config = config

    def write(self, diadefs):
        """write vcg files for <project> according to <diadefs>
        """
        for diagram in diadefs:
            basename = diagram.title.strip().replace(' ', '_')
            file_name = '%s.%s' % (basename, self.config.output_format)
            self.set_writer(file_name, basename)
            print 'creating diagram %s' % file_name
            if diagram.TYPE == 'class':
                self.write_classes(diagram)
            else:
                self.write_packages(diagram)
            self.close_graph()

    def write_packages(self, diagram):
        """write a packages diagram using the VCGPrinter"""
        for obj in diagram.modules():
            label = self.get_title(obj)
            self.printer.emit_node(obj.fig_id, label=label, shape='box')
        # package dependencies
        for rel in diagram.relationships.get('depends', ()):
            self.printer.emit_edge(rel.from_object.fig_id, rel.to_object.fig_id,
                              **self.pkg_edges)


    def write_classes(self, diagram):
        """write a classes diagram"""
        for obj in diagram.objects:
            label, shape = self.get_label(obj)
            self.printer.emit_node(obj.fig_id, label=label, shape=shape)
        # inheritance links
        for rel in diagram.relationships.get('specialization', ()):
            self.printer.emit_edge(rel.from_object.fig_id, rel.to_object.fig_id,
                              **self.inh_edges)
        # implementation links
        for rel in diagram.relationships.get('implements', ()):
            self.printer.emit_edge(rel.from_object.fig_id, rel.to_object.fig_id,
                            **self.impl_edges)
        # generate associations
        for rel in diagram.relationships.get('association', ()):
            self.printer.emit_edge(rel.from_object.fig_id, rel.to_object.fig_id,
                            label=rel.name, **self.ass_edges)


class DotWriter(DiagramWriter):
    """write dot graphs from a diagram definition and a project
    """

    def set_writer(self, file_name, basename):
        layout = dict(rankdir="BT", concentrate="true")
        self.printer = DotBackend(basename, additionnal_param=layout)
        self.file_name = file_name
        self.pkg_edges = dict(arrowtail='none', arrowhead = "open")
        self.inh_edges = dict(arrowtail = "none",arrowhead ='empty')
        self.impl_edges = dict(arrowtail="node",arrowhead ='empty',style='dashed')
        self.ass_edges = dict(fontcolor='green',arrowtail='none',arrowhead='diamond',
                                style='solid')

    def get_title(self, obj):
        return obj.title

    def get_label(self, obj):
        # TODO ? if is_exception(obj.node):
        label =  obj.title
        shape = 'record'
        if obj.shape == 'interface':
            # TODO : font italic ...
            label = "«interface»\\n%s" % label
        label = "%s|%s\l|" % (label,  r"\l".join(obj.attrs) )
        for func in obj.methods:
            label = r'%s%s()\l' % (label, func.name)
        if shape == "record":
            label = '{%s}' % label
        return label, shape

    def close_graph(self):
        self.printer.generate(self.file_name)


class VCGWriter(DiagramWriter):
    """write vcg graphs from a diagram definition and a project
    """

    def set_writer(self, file_name, basename):
        self.graph_file = open(file_name, 'w+')
        self.printer = VCGPrinter(self.graph_file)
        self.printer.open_graph(title=basename, layoutalgorithm='dfs',
                                late_edge_labels='yes', port_sharing='no',
                                manhattan_edges='yes')
        self.printer.emit_node = self.printer.node
        self.printer.emit_edge = self.printer.edge
        self.pkg_edges = dict(arrowstyle='solid', backarrowstyle='none',
                              backarrowsize=0)
        self.inh_edges = dict(arrowstyle='none',
                              backarrowstyle='solid', backarrowsize=10)
        self.impl_edges = dict(arrowstyle='none', linestyle='dotted',
                              backarrowstyle='solid', backarrowsize=10)
        self.ass_edges = dict(textcolor='black',
                              arrowstyle='none', backarrowstyle='none')

    def get_title(self, obj):
        return r'\fb%s\fn' % obj.title

    def get_label(self, obj):
        if is_exception(obj.node):
            label = r'\fb\f09%s\fn' % obj.title
        else:
            label = r'\fb%s\fn' % obj.title
        if obj.shape == 'interface':
            shape = 'ellipse'
        else:
            shape = 'box'
        attrs = obj.attrs
        methods = [func.name for func in obj.methods]
        # box width for UML like diagram
        maxlen = max(len(name) for name in [obj.title] + methods + attrs) + 2
        label = r'%s\n\f%s' % (label, "_" * maxlen)
        for attr in attrs:
            label = r'%s\n\f08%s' % (label, attr)
        if attrs:
            label = r'%s\n\f%s' % (label, "_" * maxlen)
        for func in methods:
            label = r'%s\n\f10%s()' % (label, func)
        return label, shape

    def close_graph(self):
        self.printer.close_graph()
        self.graph_file.close()

