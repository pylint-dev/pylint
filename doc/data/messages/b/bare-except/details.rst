A good rule of thumb is to limit use of bare ‘except’ clauses to two cases:
- If the exception handler will be printing out or logging the traceback; at least the user will be aware that an error has occurred.
- If the code needs to do some cleanup work, but then lets the exception propagate upwards with raise. ``try...finally`` can be a better way to handle this case.
