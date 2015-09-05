# copyright 2003-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of pylint.
#
# logilab-common is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# pylint is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with pylint.  If not, see <http://www.gnu.org/licenses/>.


class NodeNotFound(Exception):
    """raised when a node has not been found"""

EX_SIBLING_NOT_FOUND = "No such sibling as '%s'"
EX_CHILD_NOT_FOUND = "No such child as '%s'"
EX_NODE_NOT_FOUND = "No such node as '%s'"


# Base node ###################################################################

class Node(object):
    """a basic tree node, characterized by an id"""

    def __init__(self, nid=None):
        self.id = nid
        # navigation
        self.parent = None
        self.children = []

    def __iter__(self):
        return iter(self.children)

    def __str__(self, indent=0):
        s = ['%s%s %s' % (' '*indent, self.__class__.__name__, self.id)]
        indent += 2
        for child in self.children:
            try:
                s.append(child.__str__(indent))
            except TypeError:
                s.append(child.__str__())
        return '\n'.join(s)

    def is_leaf(self):
        return not self.children

    def append(self, child):
        """add a node to children"""
        self.children.append(child)
        child.parent = self

    def remove(self, child):
        """remove a child node"""
        self.children.remove(child)
        child.parent = None

    def insert(self, index, child):
        """insert a child node"""
        self.children.insert(index, child)
        child.parent = self

    def replace(self, old_child, new_child):
        """replace a child node with another"""
        i = self.children.index(old_child)
        self.children.pop(i)
        self.children.insert(i, new_child)
        new_child.parent = self

    def get_sibling(self, nid):
        """return the sibling node that has given id"""
        try:
            return self.parent.get_child_by_id(nid)
        except NodeNotFound:
            raise NodeNotFound(EX_SIBLING_NOT_FOUND % nid)

    def next_sibling(self):
        """
        return the next sibling for this node if any
        """
        parent = self.parent
        if parent is None:
            # root node has no sibling
            return None
        index = parent.children.index(self)
        try:
            return parent.children[index+1]
        except IndexError:
            return None

    def previous_sibling(self):
        """
        return the previous sibling for this node if any
        """
        parent = self.parent
        if parent is None:
            # root node has no sibling
            return None
        index = parent.children.index(self)
        if index > 0:
            return parent.children[index-1]
        return None

    def get_node_by_id(self, nid):
        """
        return node in whole hierarchy that has given id
        """
        root = self.root()
        try:
            return root.get_child_by_id(nid, 1)
        except NodeNotFound:
            raise NodeNotFound(EX_NODE_NOT_FOUND % nid)

    def get_child_by_id(self, nid, recurse=None):
        """
        return child of given id
        """
        if self.id == nid:
            return self
        for c in self.children:
            if recurse:
                try:
                    return c.get_child_by_id(nid, 1)
                except NodeNotFound:
                    continue
            if c.id == nid:
                return c
        raise NodeNotFound(EX_CHILD_NOT_FOUND % nid)

    def get_child_by_path(self, path):
        """
        return child of given path (path is a list of ids)
        """
        if len(path) > 0 and path[0] == self.id:
            if len(path) == 1:
                return self
            else:
                for c in self.children:
                    try:
                        return c.get_child_by_path(path[1:])
                    except NodeNotFound:
                        pass
        raise NodeNotFound(EX_CHILD_NOT_FOUND % path)

    def depth(self):
        """
        return depth of this node in the tree
        """
        if self.parent is not None:
            return 1 + self.parent.depth()
        else:
            return 0

    def depth_down(self):
        """
        return depth of the tree from this node
        """
        if self.children:
            return 1 + max([c.depth_down() for c in self.children])
        return 1

    def width(self):
        """
        return the width of the tree from this node
        """
        return len(self.leaves())

    def root(self):
        """
        return the root node of the tree
        """
        if self.parent is not None:
            return self.parent.root()
        return self

    def leaves(self):
        """
        return a list with all the leaves nodes descendant from this node
        """
        leaves = []
        if self.children:
            for child in self.children:
                leaves += child.leaves()
            return leaves
        else:
            return [self]

    def flatten(self, _list=None):
        """
        return a list with all the nodes descendant from this node
        """
        if _list is None:
            _list = []
        _list.append(self)
        for c in self.children:
            c.flatten(_list)
        return _list

    def lineage(self):
        """
        return list of parents up to root node
        """
        lst = [self]
        if self.parent is not None:
            lst.extend(self.parent.lineage())
        return lst


class VNode(Node):

    def get_visit_name(self):
        """
        return the visit name for the mixed class. When calling 'accept', the
        method <'visit_' + name returned by this method> will be called on the
        visitor
        """
        try:
            return self.TYPE.replace('-', '_')
        except Exception:
            return self.__class__.__name__.lower()

    def accept(self, visitor, *args, **kwargs):
        func = getattr(visitor, 'visit_%s' % self.get_visit_name())
        return func(self, *args, **kwargs)

    def leave(self, visitor, *args, **kwargs):
        func = getattr(visitor, 'leave_%s' % self.get_visit_name())
        return func(self, *args, **kwargs)
