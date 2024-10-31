.. _symilar:

Symilar
-------

The console script ``symilar`` finds copy pasted block of text in a set of files. It provides a command line interface to check only the ``duplicate-code`` message.

It can be invoked with::

  symilar [-d|--duplicates min_duplicated_lines] [-i|--ignore-comments] [--ignore-docstrings] [--ignore-imports] [--ignore-signatures] file1...

All files that shall be checked have to be passed in explicitly, e.g.::

  symilar foo.py, bar.py, subpackage/spam.py, subpackage/eggs.py

``symilar`` produces output like the following::

  17 similar lines in 2 files
  ==tests/data/clientmodule_test.py:3
  ==tests/data/suppliermodule_test.py:12
    class Ancestor:
        """ Ancestor method """
        cls_member = DoNothing()

        def __init__(self, value):
            local_variable = 0
            self.attr = 'this method shouldn\'t have a docstring'
            self.__value = value

        def get_value(self):
            """ nice docstring ;-) """
            return self.__value

        def set_value(self, value):
            self.__value = value
            return 'this method shouldn\'t have a docstring'
  TOTAL lines=58 duplicates=17 percent=29.31
