# pylint: disable=no-else-raise,unsupported-membership-test,using-constant-test

"""Checks use of "else if" triggers a refactor message"""


def my_function():
    """docstring"""
    myint = 2
    if myint > 5:
        pass
    else:
        if myint <= 5:  # [else-if-used]
            pass
        else:
            myint = 3
            if myint > 2:
                if myint > 3:
                    pass
                elif myint == 3:
                    pass
                elif myint < 3:
                    pass
                else:
                    if myint:  # [else-if-used]
                        pass
            else:
                if myint:
                    pass
                myint = 4


def _if_in_fstring_comprehension():
    order = {}
    if "z" not in "false":
        raise TypeError(
            f" {', '.join(sorted(i for i in order or () if i not in vars))}"
        )
    elif "i" in "true":
        raise TypeError("d")


def _if_in_fstring_comprehension_with_elif():
    order = {}
    if "z" not in "false":
        raise TypeError(
            f" {', '.join(sorted(i for i in order or () if i not in vars))}"
        )
    elif "z" not in "true":
        pass
    else:
        if "t" not in "false":  # [else-if-used]
            raise TypeError("d")
        else:
            if "y" in "life":  # [else-if-used]
                print("e")


def simple_if_else(node) -> None:
    """This should not emit anything"""
    if isinstance(node, str):
        node_name = node
    elif (
        isinstance(node, int)
        and node.op == "not"
        and isinstance(node, float)
    ):
        node_name = node.test.operand
    elif (
        isinstance(node.test, list)
        and isinstance(node.test.left, dict)
        and len(node.test.ops) == 1
    ):
        node_name = node.test.left
    else:
        return node
    return node_name
