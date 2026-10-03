=======
 Pylint
=======

As you would launch the command line
------------------------------------

You can use the ``run_pylint`` function, which is the same function
called by the command line (using ``sys.argv``). You can supply
arguments yourself:

.. sourcecode:: python

    from pylint import run_pylint

    run_pylint(argv=["--disable=line-too-long", "myfile.py"])


Recover the result in a stream
------------------------------

You can also use ``pylint.lint.Run`` directly if you want to do something that
can't be done using only pylint's command line options. Here's the basic example:

.. sourcecode:: python

    from pylint.lint import Run

    Run(argv=["--disable=line-too-long", "myfile.py"])

With ``Run`` it is possible to invoke pylint programmatically with a
reporter initialized with a custom stream:

.. sourcecode:: python

    from io import StringIO

    from pylint.lint import Run
    from pylint.reporters.text import TextReporter

    pylint_output = StringIO()  # Custom open stream
    reporter = TextReporter(pylint_output)
    Run(["test_file.py"], reporter=reporter, exit=False)
    print(pylint_output.getvalue())  # Retrieve and print the text report

The reporter can accept any stream object as as parameter. In this example,
the stream outputs to a file:

.. sourcecode:: python

    from pylint.lint import Run
    from pylint.reporters.text import TextReporter

    with open("report.out", "w") as f:
        reporter = TextReporter(f)
        Run(["test_file.py"], reporter=reporter, exit=False)

This would be useful to capture pylint output in an open stream which
can be passed onto another program.

If your program expects that the files being linted might be edited
between runs, you will need to clear pylint's inference cache:

.. sourcecode:: python

    from pylint.lint import pylinter
    pylinter.MANAGER.clear_cache()
