In Python 2.7, ``super()`` has to be called with its own class and ``self`` as arguments (``super(Cat, self)``), which can
lead to a mix up of parent and child class in the code.

In Python 3 the recommended way is to call ``super()`` without arguments (see also ``super-with-arguments``).
