Say you have a file called ``my_file.py``. ``import-self`` would be raised on the following code::


    from my_file import a_function  # [import-self]

    def a_function():
        pass

The solution would be to remove the import::

    def a_function():
        pass
