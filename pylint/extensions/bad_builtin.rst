This used to be the ``bad-builtin`` core checker, but it was moved to
an extension instead. It can be used for finding prohibited used builtins,
such as ``map`` or ``filter``, for which other alternatives exists.

If you want to control for what builtins the checker should warn about,
you can use the ``bad-functions`` option::

    $ pylint a.py --load-plugins=pylint.extensions.bad_builtin --bad-functions=apply,reduce
    ...
