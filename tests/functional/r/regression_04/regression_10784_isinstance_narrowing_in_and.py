"""Regression test for https://github.com/pylint-dev/pylint/issues/10784

On the right of ``isinstance(x, A) and``, ``x`` is an ``A``, even when an
unrelated assignment elsewhere gives it another type.
"""

# pylint: disable=missing-docstring,too-few-public-methods


class Statement:
    pass


class Expression:
    pass


class Assignment(Statement):
    source: Expression


class Jump(Statement):
    pass


class BinaryOp(Expression):
    pass


class Block:
    statements: list[Statement]


def make_block() -> Block:
    block = Block()
    block.statements = [Jump()]
    return block


def check_block():
    block = Block()
    for statement in block.statements:
        if isinstance(statement, Assignment) and isinstance(statement.source, BinaryOp):
            print("assignment")
