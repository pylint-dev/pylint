In Python 2.7, ``super()`` has to be called with the own class and ``self`` as arguments (``super(Bar, self)``), which can
lead to a mix up of parent and child class in the code.

In Python 3 the recommended way is to user ``super()`` without arguments (see also ``super-with-arguments``).
