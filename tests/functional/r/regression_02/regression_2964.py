"""
Regression test for `no-member`.
See: https://github.com/pylint-dev/pylint/issues/2964
"""

# pylint: disable=missing-class-docstring,too-few-public-methods
# pylint: disable=unused-private-member,protected-access


class Node:
    def __init__(self, name, path=()):
        """
        Initialize self with "name" string and the tuple "path" of its parents.
        "self" is added to the tuple as its last item.
        """
        self.__name = name
        self.__path = path + (self,)

    def get_full_name(self):
        """
        A `no-member` message was emitted:
        nodes.py:17:24: E1101: Instance of 'tuple' has no '__name' member (no-member)
        """
        return ".".join(node.__name for node in self.__path)
