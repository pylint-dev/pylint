# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE


import astroid

from pylint import checkers, interfaces
from pylint.checkers import utils
from pylint.constants import BUILTINS


class NotChecker(checkers.BaseChecker):
    """checks for too many not in comparison expressions

    - "not not" should trigger a warning
    - "not" followed by a comparison should trigger a warning
    """

    __implements__ = (interfaces.IAstroidChecker,)
    msgs = {
        "C0113": (
            'Consider changing "%s" to "%s"',
            "unneeded-not",
            "Used when a boolean expression contains an unneeded negation.",
        )
    }
    name = "refactoring"
    reverse_op = {
        "<": ">=",
        "<=": ">",
        ">": "<=",
        ">=": "<",
        "==": "!=",
        "!=": "==",
        "in": "not in",
        "is": "is not",
    }
    # sets are not ordered, so for example "not set(LEFT_VALS) <= set(RIGHT_VALS)" is
    # not equivalent to "set(LEFT_VALS) > set(RIGHT_VALS)"
    skipped_nodes = (astroid.Set,)
    # 'builtins' py3, '__builtin__' py2
    skipped_classnames = [f"{BUILTINS}.{qname}" for qname in ("set", "frozenset")]

    @utils.check_messages("unneeded-not")
    def visit_unaryop(self, node):
        if node.op != "not":
            return
        operand = node.operand

        if isinstance(operand, astroid.UnaryOp) and operand.op == "not":
            self.add_message(
                "unneeded-not",
                node=node,
                args=(node.as_string(), operand.operand.as_string()),
            )
        elif isinstance(operand, astroid.Compare):
            left = operand.left
            # ignore multiple comparisons
            if len(operand.ops) > 1:
                return
            operator, right = operand.ops[0]
            if operator not in self.reverse_op:
                return
            # Ignore __ne__ as function of __eq__
            frame = node.frame()
            if frame.name == "__ne__" and operator == "==":
                return
            for _type in (utils.node_type(left), utils.node_type(right)):
                if not _type:
                    return
                if isinstance(_type, self.skipped_nodes):
                    return
                if (
                    isinstance(_type, astroid.Instance)
                    and _type.qname() in self.skipped_classnames
                ):
                    return
            suggestion = "{} {} {}".format(
                left.as_string(),
                self.reverse_op[operator],
                right.as_string(),
            )
            self.add_message(
                "unneeded-not", node=node, args=(node.as_string(), suggestion)
            )
