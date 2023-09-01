###
API
###

You can call ``Pylint``, ``symilar`` and ``pyreverse`` from another
Python program thanks to their APIs:

.. sourcecode:: python

    from pylint import run_pylint, run_pyreverse, run_symilar

    run_pylint("--disable=C", "myfile.py")
    run_pyreverse(...)
    run_symilar(...)


.. toctree::
  :maxdepth: 1
  :hidden:

  pylint
