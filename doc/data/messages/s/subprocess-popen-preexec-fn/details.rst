The `preexec_fn` parameter is not safe to use in the presence of threads in
your application. The child process could deadlock before `exec` is called. If
you must use it, keep it trivial! Minimize the number of libraries you call
into.
