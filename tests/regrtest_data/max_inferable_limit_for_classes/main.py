"""This example is based on sqlalchemy.

See https://github.com/pylint-dev/pylint/issues/5679
"""
from other_funcs import FromClause

from .nodes import roles


class HasMemoized(object):
    ...


class Generative(HasMemoized):
    ...


class ColumnElement(
    roles.ColumnArgumentOrKeyRole,
    roles.BinaryElementRole,
    roles.OrderByRole,
    roles.ColumnsClauseRole,
    roles.LimitOffsetRole,
    roles.DMLColumnRole,
    roles.DDLConstraintColumnRole,
    roles.StatementRole,
    Generative,
):
    ...


class FunctionElement(ColumnElement, FromClause):
    ...


class months_between(FunctionElement):
    def __init__(self):
        super().__init__()
