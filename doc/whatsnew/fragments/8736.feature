``comparison-of-constants`` now use the unicode from the ast instead of reformatting from
 the node's values preventing some bad formatting due to ``utf-8`` limitation. The message now use
 ``"`` instead of ``'`` to better work with what the python ast returns.

Refs #8736
