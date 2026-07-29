This message is disabled by default, because ``py-version`` defaults to the
interpreter running pylint rather than to the oldest interpreter you support.

It is meant to be run once, when you drop the maintenance of a Python
interpreter: bump ``py-version`` to the oldest version you still support, then
do a single pass with ``pylint --enable=useless-version-check`` to find the checks
that became dead code. Keeping it on permanently buys you little, as no new
occurrence appears until the next version you drop.

Only the lower bound can be decided: nothing prevents your code from running on
an interpreter newer than any version you know about, so ``sys.version_info >=
(3, 42)`` is never reported. For the same reason ``sys.version_info.minor`` is
left alone, as it goes back to 0 on a new major release.

Only the ``sys.version_info`` attribute is recognized: a name imported with
``from sys import version_info`` is not reported. This keeps the check simple,
and the attribute is by far the most common way to write the comparison.
