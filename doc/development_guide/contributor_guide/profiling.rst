.. -*- coding: utf-8 -*-
.. _profiling:

===================================
 Profiling and performance analysis
===================================

Performance analysis for Pylint
-------------------------------

To analyse the performance of Pylint we recommend to use the ``cProfile`` module
from ``stdlib``. Together with the ``pstats`` module this should give you all the tools
you need to profile a Pylint run and see which functions take how long to run.

The documentation for both modules can be found at cProfile_.

To profile a run of Pylint over itself you can use the following code and run it from the base directory.
Note that ``cProfile`` will create a document called ``stats`` that is then read by ``pstats``. The
human-readable output will be stored by ``pstats`` in ``./profiler_stats``. It will be sorted by
``cumulative time``:

.. sourcecode:: python

    import cProfile
    import pstats
    import sys

    sys.argv = ["pylint", "pylint"]
    cProfile.run("from pylint import __main__", "stats")

    with open("profiler_stats", "w", encoding="utf-8") as file:
        stats = pstats.Stats("stats", stream=file)
        stats.sort_stats("cumtime")
        stats.print_stats()

You can also interact with the stats object by sorting or restricting the output.
For example, to only print functions from the ``pylint`` module and sort by cumulative time you could
use:

.. sourcecode:: python

    import cProfile
    import pstats
    import sys

    sys.argv = ["pylint", "pylint"]
    cProfile.run("from pylint import __main__", "stats")

    with open("profiler_stats", "w", encoding="utf-8") as file:
        stats = pstats.Stats("stats", stream=file)
        stats.sort_stats("cumtime")
        stats.print_stats("pylint/pylint")

Lastly, to profile a run over your own module or code you can use:

.. sourcecode:: python

    import cProfile
    import pstats
    import sys

    sys.argv = ["pylint", "your_dir/your_file"]
    cProfile.run("from pylint import __main__", "stats")

    with open("profiler_stats", "w", encoding="utf-8") as file:
        stats = pstats.Stats("stats", stream=file)
        stats.sort_stats("cumtime")
        stats.print_stats()

The documentation of the ``pstats`` module discusses other possibilities to interact with
the profiling output.


Performance analysis of a specific checker
------------------------------------------

To analyse the performance of specific checker within Pylint we can use the human-readable output
created by ``pstats``.

If you search in the ``profiler_stats`` file for the file name of the checker you will find all functional
calls from functions within the checker. Let's say we want to check the ``visit_importfrom`` method of the
``variables`` checker::

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    622    0.006    0.000    8.039    0.013 /MY_PROGRAMMING_DIR/pylint/pylint/checkers/variables.py:1445(visit_importfrom)

The previous line tells us that this method was called 622 times during the profile and we were inside the
function itself for 6 ms in total. The time per call is less than a millisecond (0.006 / 622)
and thus is displayed as being 0.

Often you are more interested in the cumulative time (per call). This refers to the time spent within the function
and any of the functions it called or the functions they called (etc.). In our example, the ``visit_importfrom``
method and all of its child-functions took a little over 8 seconds to execute, with an execution time of
0.013 ms per call.

You can also search the ``profiler_stats`` for an individual function you want to check. For example
``_analyse_fallback_blocks``, a function called by ``visit_importfrom`` in the ``variables`` checker. This
allows more detailed analysis of specific functions::

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1    0.000    0.000    0.000    0.000 /MY_PROGRAMMING_DIR/pylint/pylint/checkers/variables.py:1511(_analyse_fallback_blocks)


Parsing the profiler stats with other tools
-------------------------------------------

Often you might want to create a visual representation of your profiling stats. A good tool
to do this is gprof2dot_. This tool can create a ``.dot`` file from the profiling stats
created by ``cProfile`` and ``pstats``. You can then convert the ``.dot`` file to a ``.png``
file with one of the many converters found online.

You can read the gprof2dot_ documentation for installation instructions for your specific environment.

Another option would be snakeviz_.

.. _cProfile: https://docs.python.org/3/library/profile.html
.. _gprof2dot: https://github.com/jrfonseca/gprof2dot
.. _snakeviz: https://jiffyclub.github.io/snakeviz/
