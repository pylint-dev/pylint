You can now use this plugin for finding complexity issues in your code base.

Activate it through ``pylint --load-plugins=pylint.extensions.mccabe``. It introduces
a new warning, ``too-complex``, which is emitted when a code block has a complexity
higher than a preestablished value, which can be controlled through the
``max-complexity`` option, such as in this example::

    $ cat a.py
    def f10():
        """McCabe rating: 11"""
        myint = 2
        if myint == 5:
            return myint
        elif myint == 6:
            return myint
        elif myint == 7:
            return myint
        elif myint == 8:
            return myint
        elif myint == 9:
            return myint
        elif myint == 10:
            if myint == 8:
                while True:
                    return True
            elif myint == 8:
                with myint:
                    return 8
        else:
            if myint == 2:
                return myint
            return myint
        return myint
    $ pylint a.py --load-plugins=pylint.extensions.mccabe
    R:1: 'f10' is too complex. The McCabe rating is 11 (too-complex)
    $ pylint a.py --load-plugins=pylint.extensions.mccabe --max-complexity=50
    $
