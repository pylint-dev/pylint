When the message names an ``elif``, the diagnostic is attached to the ``if``
whose branch cannot fall through. Change only the first ``elif`` following that
reported branch to ``if``. Any later ``elif`` and ``else`` clauses remain
attached to the new ``if`` during this transformation.

If another branch in the remaining chain also cannot fall through, a later
Pylint run may report that branch separately. Each diagnostic describes one
transformation; it does not ask you to change every ``elif`` at once.

For example, after changing the first ``elif`` below, the remaining clauses
still form one mutually exclusive chain::

    if value is None:
        return "missing"
    if value < 0:
        description = "negative"
    elif value == 0:
        return "zero"
    else:
        description = "positive"
    return description

This check only identifies redundant control-flow nesting. It cannot decide
whether keeping an ``elif`` makes a deliberately exhaustive decision tree easier
for readers to recognize. If that structure is clearer for a particular case,
keep it and disable the message locally on the reported ``if`` statement::

    if value is None:  # pylint: disable=no-else-return
        return "missing"
    elif value < 0:
        return "negative"
    else:
        return "non-negative"
