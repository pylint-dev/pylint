Passing a whole object when only one part of it is needed ties the function
to the object's structure for no benefit: this is sometimes called *stamp
coupling*. Callers must build (or know about) the whole object even when they
only have the one value the function really needs. Accepting the value itself
(*data coupling*) keeps the function independent.

By default only private and nested functions are checked, because narrowing a
public signature is a breaking change for callers: set
``suggest-narrowing-public-parameters`` to ``yes`` to check public functions
and methods too.

Functions whose signature is imposed by a convention or a framework can be
excluded with the ``ignored-function-names`` option — for example visitor
callbacks, or pytest test functions whose parameters are fixtures injected by
name::

    [REFACTORING]
    ignored-function-names=(visit_|leave_|test_|pytest_).*
