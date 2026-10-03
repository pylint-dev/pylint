"""Tests for no-member for self-referencing instance attributes
See https://github.com/pylint-dev/pylint/issues/1555
"""
# pylint: disable=too-few-public-methods


class ClassWithMember:
    """Member defined in superclass."""
    def __init__(self):
        self.member = True


class AssignMemberInSameLine:
    """This class attempts to assign and access a member in the same line."""
    def __init__(self):
        self.member = self.member  # [no-member]


class AssignMemberInSameLineAfterTypeAnnotation:
    """This might emit a message like `maybe-no-member` in the future."""
    def __init__(self):
        self.member: bool
        self.member = self.member


class AssignMemberFromSuper1(ClassWithMember):
    """This assignment is valid due to inheritance."""
    def __init__(self):
        self.member = self.member
        super().__init__()


class AssignMemberFromSuper2(ClassWithMember):
    """This assignment is valid due to inheritance."""
    def __init__(self):
        super().__init__()
        self.member = self.member
