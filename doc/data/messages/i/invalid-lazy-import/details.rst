A ``lazy`` import (`PEP 810 <https://peps.python.org/pep-0810/>`_) is only
allowed at module level, outside of any ``try`` statement, and never as a
wildcard import. Python raises a ``SyntaxError`` for the other positions, but
only when the module is compiled: the standard library's ``ast`` module parses
them without complaining, so ``pylint`` reports them itself.
