# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/10784

Chaining type narrowing checks with ``and`` should not emit ``no-member``
for attributes accessed in subsequent checks.
"""

# pylint: disable=missing-docstring,too-few-public-methods


class Statement:
    pass


class Expression:
    pass


class Assignment(Statement):
    src: Expression


class ConditionalJump(Statement):
    pass


class BinaryOp(Expression):
    op: str


class Block:
    statements: list[Statement]


def make_block_with_conditional_jump() -> Block:
    cond_block = Block()
    cond_block.statements = [ConditionalJump()]
    return cond_block


def check_block_local() -> None:
    block = Block()
    for stmt in block.statements:
        if isinstance(stmt, Assignment) and isinstance(stmt.src, BinaryOp):
            print("Assignment")


def check_block_and_attr() -> None:
    block = Block()
    for stmt in block.statements:
        if isinstance(stmt, Assignment) and stmt.src:
            print("Assignment with src")
