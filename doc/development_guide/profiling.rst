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
It will store the profiling data in ``./profiler_stats``::

    import cProfile
    import pstats
    import sys
    from pstats import SortKey

    sys.argv = ["pylint", "pylint"]
    cProfile.run("from pylint import __main__", "stats")

    with open("profiler_stats", "w", encoding="utf-8") as file:
        stats = pstats.Stats("stats", stream=file)
        stats.print_stats()

You can also interact with the stats object by sorting or restricting the output.
For example, to only print functions from the ``pylint`` module and sort by cumulative time you could
use::

    import cProfile
    import pstats
    import sys
    from pstats import SortKey

    sys.argv = ["pylint", "pylint"]
    cProfile.run("from pylint import __main__", "stats")

    with open("profiler_stats", "w", encoding="utf-8") as file:
        stats = pstats.Stats("stats", stream=file)
        stats.sort_stats("cumtime")
        stats.print_stats("pylint/pylint")

Lastly, to profile a run over your own module or code you can use::

    import cProfile
    import pstats
    import sys
    from pstats import SortKey

    sys.argv = ["pylint", "your_dir/your_file"]
    cProfile.run("from pylint import __main__", "stats")

    with open("profiler_stats", "w", encoding="utf-8") as file:
        stats = pstats.Stats("stats", stream=file)
        stats.print_stats()

The documentation of the ``pstats`` module discusses other possibilites to interact with
the profiling output.


.. _cProfile: https://docs.python.org/3/library/profile.html
