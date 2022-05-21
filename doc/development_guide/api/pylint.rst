=======
 Pylint
=======

You can call Pylint from another Python program thanks to the ``Run()``
class in the ``pylint.lint`` module
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
