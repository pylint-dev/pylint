===========================================
 Running Pylint from another python program
===========================================

You can call Pylint from another Python program thanks to the ``Run()``
function in the ``pylint.lint`` module
(assuming Pylint options are stored in a list of strings ``pylint_options``) as:

.. sourcecode:: python

  import pylint.lint
  pylint_opts = ['--disable=line-too-long', 'myfile.py']
  pylint.lint.Run(pylint_opts)

Another option would be to use the ``run_pylint`` function, which is the same function
called by the command line. You can either patch ``sys.argv`` or supply arguments yourself:

.. sourcecode:: python

  import pylint

  sys.argv = ["pylint", "your_file"]
  pylint.run_pylint()
  # Or:
  pylint.run_pylint(argv=["your_file"])

To silently run Pylint on a ``module_name.py`` module,
and get its standard output and error:

.. sourcecode:: python

  from pylint import epylint as lint

  (pylint_stdout, pylint_stderr) = lint.py_run('module_name.py', return_std=True)

It is also possible to include additional Pylint options in the first argument to ``py_run``:

.. sourcecode:: python

  from pylint import epylint as lint

  (pylint_stdout, pylint_stderr) = lint.py_run('module_name.py --disable C0114', return_std=True)

The options ``--msg-template="{path}:{line}: {category} ({msg_id}, {symbol}, {obj}) {msg}"`` and
``--reports=n`` are set implicitly inside the ``epylint`` module.

Finally, it is possible to invoke pylint programmatically with a
reporter initialized with a custom stream:

.. sourcecode:: python

    from io import StringIO

    from pylint.lint import Run
    from pylint.reporters.text import TextReporter

    pylint_output = StringIO()  # Custom open stream
    reporter = TextReporter(pylint_output)
    Run(["test_file.py"], reporter=reporter, do_exit=False)
    print(pylint_output.getvalue())  # Retrieve and print the text report

The reporter can accept any stream object as as parameter. In this example,
the stream outputs to a file:

.. sourcecode:: python

    from pylint.lint import Run
    from pylint.reporters.text import TextReporter

    with open("report.out", "w") as f:
        reporter = TextReporter(f)
        Run(["test_file.py"], reporter=reporter, do_exit=False)

This would be useful to capture pylint output in an open stream which
can be passed onto another program.

If your program expects that the files being linted might be edited
between runs, you will need to clear pylint's inference cache:

.. sourcecode:: python

    from pylint.lint import pylinter
    pylinter.MANAGER.clear_cache()
