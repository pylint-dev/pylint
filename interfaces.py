# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""Interfaces for Pylint objects"""
from collections import namedtuple

from logilab.common.interface import Interface

Confidence = namedtuple('Confidence', ['name', 'description'])
# Warning Certainties
HIGH = Confidence('HIGH', 'No false positive possible.')
INFERENCE = Confidence('INFERENCE', 'Warning based on inference result.')
INFERENCE_FAILURE = Confidence('INFERENCE_FAILURE',
                               'Warning based on inference with failures.')
UNDEFINED = Confidence('UNDEFINED',
                       'Warning without any associated confidence level.')

CONFIDENCE_LEVELS = [HIGH, INFERENCE, INFERENCE_FAILURE, UNDEFINED]


class IChecker(Interface):
    """This is an base interface, not designed to be used elsewhere than for
    sub interfaces definition.
    """

    def open(self):
        """called before visiting project (i.e set of modules)"""

    def close(self):
        """called after visiting project (i.e set of modules)"""


class IRawChecker(IChecker):
    """interface for checker which need to parse the raw file
    """

    def process_module(self, astroid):
        """ process a module

        the module's content is accessible via astroid.stream
        """


class ITokenChecker(IChecker):
    """Interface for checkers that need access to the token list."""
    def process_tokens(self, tokens):
        """Process a module.

        tokens is a list of all source code tokens in the file.
        """


class IAstroidChecker(IChecker):
    """ interface for checker which prefers receive events according to
    statement type
    """


class IReporter(Interface):
    """ reporter collect messages and display results encapsulated in a layout
    """
    def add_message(self, msg_id, location, msg):
        """add a message of a given type

        msg_id is a message identifier
        location is a 3-uple (module, object, line)
        msg is the actual message
        """

    def display_results(self, layout):
        """display results encapsulated in the layout tree
        """


__all__ = ('IRawChecker', 'IAstroidChecker', 'ITokenChecker', 'IReporter')
