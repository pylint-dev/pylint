Duplicate argument names in function definitions are syntax errors.

.. code:: python
    
    >>> def get_fruits(apple, banana, apple):  # [duplicate-argument-name]
    ...     pass
    ...
    File "<stdin>", line 1
    SyntaxError: duplicate argument 'apple' in function definition
    >>>
