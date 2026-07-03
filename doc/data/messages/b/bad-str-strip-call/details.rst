A common misconception is that ``str.strip('Hello')`` removes the *substring* ``'Hello'`` from the beginning and end of the string.
This is **not**  the case.
From the `documentation <https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip>`_:

> The chars argument is not a prefix or suffix; rather, all combinations of its values are stripped

Duplicated characters in the ``str.strip`` call, besides not having any effect on the actual result, may indicate this misunderstanding.
