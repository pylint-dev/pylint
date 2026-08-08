"""Functions matching ignored-function-names follow a signature convention."""

# pylint: disable=missing-docstring,too-few-public-methods


class ColorVisitor:
    def visit_assign(self, node):
        return node.value

    def leave_assign(self, node):
        return node.value
