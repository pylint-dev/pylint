=======
epylint
=======

To silently run epylint on a ``module_name.py`` module, and get its standard output and error:

.. sourcecode:: python

  from pylint import epylint as lint

  (pylint_stdout, pylint_stderr) = lint.py_run('module_name.py', return_std=True)

It is also possible to include additional Pylint options in the first argument to ``py_run``:

.. sourcecode:: python

  from pylint import epylint as lint

  (pylint_stdout, pylint_stderr) = lint.py_run('module_name.py --disable C0114', return_std=True)

The options ``--msg-template="{path}:{line}: {category} ({msg_id}, {symbol}, {obj}) {msg}"`` and
``--reports=n`` are set implicitly inside the ``epylint`` module.
