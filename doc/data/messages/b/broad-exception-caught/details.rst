If you use a naked ``except Exception:`` clause, you might end up catching exceptions other than the ones you expect to catch
This can hide bugs or make it harder to debug programs when they aren't doing what you expect.

For example, you're trying to import a library with required system dependencies and you catch
everything instead of only import errors, you will miss the error message telling you, that
your code could work if you had installed the system dependencies.
