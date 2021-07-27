# pylint: disable=missing-docstring, too-few-public-methods, invalid-name

# Inheritance diagram:
#       F
#      /
#  D  E
#   \/
#    B  C
#     \/
#      A
#
# Once `E` is pruned from the tree, we have:
#  D
#   \
#    B  C
#     \/
#      A
#
# By setting `max-parents=2`, we're able to check that tree-pruning works
# correctly; in the new diagram, `B` has only 1 parent, so it doesn't raise a
# message, and `A` has 3, so it does raise a message with the specific number
# of parents.

class F:
    """0 parents"""

class E(F):
    """1 parent"""

class D:
    """0 parents"""

class B(D, E):
    """3 parents"""

class C:
    """0 parents"""

class A(B, C): # [too-many-ancestors]
    """5 parents"""
