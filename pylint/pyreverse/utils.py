# Copyright (c) 2002-2013 LOGILAB S.A. (Paris, FRANCE).
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
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
generic classes/functions for pyreverse core/extensions
"""
from __future__ import print_function

import sys
import re
import os

########### pyreverse option utils ##############################


RCFILE = '.pyreverserc'

def get_default_options():
    """
    Read config file and return list of options
    """
    options = []
    home = os.environ.get('HOME', '')
    if home:
        rcfile = os.path.join(home, RCFILE)
        try:
            options = open(rcfile).read().split()
        except IOError:
            pass # ignore if no config file found
    return options

def insert_default_options():
    """insert default options to sys.argv
    """
    options = get_default_options()
    options.reverse()
    for arg in options:
        sys.argv.insert(1, arg)



# astroid utilities ###########################################################

SPECIAL = re.compile('^__[A-Za-z0-9]+[A-Za-z0-9_]*__$')
PRIVATE = re.compile('^__[_A-Za-z0-9]*[A-Za-z0-9]+_?$')
PROTECTED = re.compile('^_[_A-Za-z0-9]*$')

def get_visibility(name):
    """return the visibility from a name: public, protected, private or special
    """
    if SPECIAL.match(name):
        visibility = 'special'
    elif PRIVATE.match(name):
        visibility = 'private'
    elif PROTECTED.match(name):
        visibility = 'protected'

    else:
        visibility = 'public'
    return visibility

ABSTRACT = re.compile('^.*Abstract.*')
FINAL = re.compile('^[A-Z_]*$')

def is_abstract(node):
    """return true if the given class node correspond to an abstract class
    definition
    """
    return ABSTRACT.match(node.name)

def is_final(node):
    """return true if the given class/function node correspond to final
    definition
    """
    return FINAL.match(node.name)

def is_interface(node):
    # bw compat
    return node.type == 'interface'

def is_exception(node):
    # bw compat
    return node.type == 'exception'


# Helpers #####################################################################

_CONSTRUCTOR = 1
_SPECIAL = 2
_PROTECTED = 4
_PRIVATE = 8
MODES = {
    'ALL'       : 0,
    'PUB_ONLY'  : _SPECIAL + _PROTECTED + _PRIVATE,
    'SPECIAL'   : _SPECIAL,
    'OTHER'     : _PROTECTED + _PRIVATE,
}
VIS_MOD = {'special': _SPECIAL, 'protected': _PROTECTED,
           'private': _PRIVATE, 'public': 0}

class FilterMixIn(object):
    """filter nodes according to a mode and nodes' visibility
    """
    def __init__(self, mode):
        "init filter modes"
        __mode = 0
        for nummod in mode.split('+'):
            try:
                __mode += MODES[nummod]
            except KeyError as ex:
                print('Unknown filter mode %s' % ex, file=sys.stderr)
        self.__mode = __mode


    def show_attr(self, node):
        """return true if the node should be treated
        """
        visibility = get_visibility(getattr(node, 'name', node))
        return not self.__mode & VIS_MOD[visibility]

