from operator import attrgetter

from .nodes import roles


class HasCacheKey(object):
    ...


class HasMemoized(object):
    ...


class MemoizedHasCacheKey(HasCacheKey, HasMemoized):
    ...


class ClauseElement(MemoizedHasCacheKey):
    ...


class ReturnsRows(roles.ReturnsRowsRole, ClauseElement):
    ...


class Selectable(ReturnsRows):
    ...


class FromClause(roles.AnonymizedFromClauseRole, Selectable):
    c = property(attrgetter("columns"))
