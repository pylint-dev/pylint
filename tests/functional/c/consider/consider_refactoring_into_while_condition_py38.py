"""Emit a message for breaking out of a while True loop immediately."""
# pylint: disable=missing-function-docstring,missing-class-docstring,unrecognized-inline-option,invalid-name,literal-comparison, undefined-variable, too-many-public-methods, too-few-public-methods

class Issue8015:
    def test_assignment_expr(self):
        b = 10
        while True:  # [consider-refactoring-into-while-condition]
            if (a := 10) == (a := 10):
                break
        while True:  # [consider-refactoring-into-while-condition]
            if (a if a == 10 else 0) == (b if b == 10 else 0):
                break
