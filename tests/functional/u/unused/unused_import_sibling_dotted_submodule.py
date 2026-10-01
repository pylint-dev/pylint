"""Sibling dotted-submodule imports must be checked independently.

`import fake.bar` and `import fake.foo` both bind the local name `fake`, so
using one of them must not hide the other one being unused.

    https://github.com/pylint-dev/pylint/issues/2583
"""

# pylint: disable=missing-docstring, import-error

import fake.bar  # [unused-import]
import fake.foo

# Siblings that share a deeper prefix (e.g. ``email.mime.application`` and
# ``email.mime.multipart``) must be told apart too: a used sibling must not be
# flagged, and an unused one must be, even though both start with ``deep.mime``.
import deep.mime.application  # [unused-import]
import deep.mime.multipart

fake.foo.do_something()
deep.mime.multipart.build()
