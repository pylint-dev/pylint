Add ``nonsensical-float-arg``, emitted when infinity or NaN is passed to a parameter
that has no sensible behaviour for it, such as a comparison tolerance, a timeout or a
conversion to an integer. The check is built as a mixin so a plugin can register the
arguments of its own library.

Closes #11220
