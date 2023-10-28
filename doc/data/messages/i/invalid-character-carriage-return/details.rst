This message exists because one of our checkers is very generic, but it's never going to
raise during normal use as it's a ``syntax-error`` that would prevent the python ast
(and thus pylint) from constructing a code representation of the file.

You could encounter it by feeding a properly constructed node directly to the checker.
