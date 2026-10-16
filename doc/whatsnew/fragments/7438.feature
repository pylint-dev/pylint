Add the ``--fix`` option to apply the automatic fixes of messages, with
``--unsafe-fixes``, ``--fix-diff`` and ``--unfixable`` to control it. Checkers
can attach a fix to a message with ``add_message(..., fix=...)``, and the
``json2`` output now includes the fix of each message. No message has a fix yet,
they will be added message by message.

Refs #7438
