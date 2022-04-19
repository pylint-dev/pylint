class SQLRole(object):
    ...


class UsesInspection(object):
    ...


class AllowsLambdaRole(object):
    ...


class ColumnArgumentRole(SQLRole):
    ...


class ColumnArgumentOrKeyRole(ColumnArgumentRole):
    ...


class ColumnListRole(SQLRole):
    ...


class ColumnsClauseRole(AllowsLambdaRole, UsesInspection, ColumnListRole):
    ...


class LimitOffsetRole(SQLRole):
    ...


class ByOfRole(ColumnListRole):
    ...


class OrderByRole(AllowsLambdaRole, ByOfRole):
    ...


class StructuralRole(SQLRole):
    ...


class ExpressionElementRole(SQLRole):
    ...


class BinaryElementRole(ExpressionElementRole):
    ...


class JoinTargetRole(AllowsLambdaRole, UsesInspection, StructuralRole):
    ...


class FromClauseRole(ColumnsClauseRole, JoinTargetRole):
    ...


class StrictFromClauseRole(FromClauseRole):
    ...


class AnonymizedFromClauseRole(StrictFromClauseRole):
    ...


class ReturnsRowsRole(SQLRole):
    ...


class StatementRole(SQLRole):
    ...


class DMLColumnRole(SQLRole):
    ...


class DDLConstraintColumnRole(SQLRole):
    ...
