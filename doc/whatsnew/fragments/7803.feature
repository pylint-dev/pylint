Add ``useless-version-check`` (``W2607``), a message disabled by default that reports
``sys.version_info`` comparisons whose outcome is the same for every interpreter
allowed by the ``py-version`` setting, i.e. checks guarding dead code.

Closes #7803
