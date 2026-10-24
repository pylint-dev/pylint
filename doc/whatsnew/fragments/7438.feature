Add the ``--fix`` option to apply the automatic fixes of messages, with
``--unsafe-fixes``, ``--fix-diff`` and ``--unfixable`` to control it. Checkers
can attach a fix to a message with ``add_message(..., fix=...)``, and the
``json2`` output now includes the fix of each message.

``use-a-generator`` is the first message with a fix: ``any([x for x in y])``
becomes ``any(x for x in y)``. The fix is unsafe because the generator stops at
the first value deciding the result, so it needs ``--unsafe-fixes``.

Refs #7438
