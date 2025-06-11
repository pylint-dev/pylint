"""Functional tests for the ``unreachable-match-patterns`` message"""


a = 'a'
b = 'b'
s = 'a'


match s:
    case a:  # [unreachable-match-patterns]
        pass
    case b:  # [unreachable-match-patterns]
        pass
    case s:
        pass
