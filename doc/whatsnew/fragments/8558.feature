Add a new checker ``hidden-kwarg`` to warn when a function is called with a keyword argument which shares a name with a positional-only parameter and the function contains a keyword variadic parameter dictionary. It may be surprising behaviour when the keyword argument is added to the keyword variadic parameter dictionary.

Closes #8558
