Lazy imports were introduced in Python 3.15, and older versions cannot compile a
module that contains one. This message is emitted as long as the ``py-version``
setting still includes one of those older versions.

Once you no longer support them, raise ``py-version`` to 3.15. Until then, use a
regular ``import``: placing it inside the function that needs it also delays it
until that function runs.
