Instantiating and using a contextmanager inside a generator function can
result in unexpected behavior if there is an expectation that the context is only
available for the generator function. In the case that the generator is not closed or destroyed
then the context manager is held suspended as is.

This message warns on the generator function instead of the contextmanager function
because the ways to use a contextmanager are many.
A contextmanager can be used as a decorator (which immediately has ``__enter__``/``__exit__`` applied)
and the use of ``as ...`` or discard of the return value also implies whether the context needs cleanup or not.
So for this message, warning the invoker of the contextmanager is important.
