# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import astroid

from pylint.checkers.refactoring import LenChecker


def test_class_tree_detection():
    module = astroid.parse(
        """
class ClassWithBool(list):
    def __bool__(self):
        return True

class ClassWithoutBool(dict):
    pass

class ChildClassWithBool(ClassWithBool):
    pass

class ChildClassWithoutBool(ClassWithoutBool):
    pass
"""
    )
    with_bool, without_bool, child_with_bool, child_without_bool = module.body
    assert LenChecker().base_classes_of_node(with_bool) == [
        "ClassWithBool",
        "list",
        "object",
    ]
    assert LenChecker().base_classes_of_node(without_bool) == [
        "ClassWithoutBool",
        "dict",
        "object",
    ]
    assert LenChecker().base_classes_of_node(child_with_bool) == [
        "ChildClassWithBool",
        "ClassWithBool",
        "list",
        "object",
    ]
    assert LenChecker().base_classes_of_node(child_without_bool) == [
        "ChildClassWithoutBool",
        "ClassWithoutBool",
        "dict",
        "object",
    ]
