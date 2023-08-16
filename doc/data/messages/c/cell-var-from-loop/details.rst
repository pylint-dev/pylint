It is also possible to use `functools.partial` to avoid this error::

    def foo(numbers):
        for i in numbers:

            def bar():
                functools.partial(print, i)()

            bar()
