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

# A name bound by a single dotted import is handled by the normal machinery; the
# sibling recovery must leave it alone (there is no sibling to tell apart).
import lonely.only

# When *no* sibling bound to the shared name is used, both imports are already
# reported as unused by the normal machinery and recovery must not interfere.
import neither.alpha  # [unused-import]
import neither.beta  # [unused-import]

# A bare reference to the shared name (not an attribute access) could reach any
# of the siblings, so none of them may be reported as unused for that name.
import ambiguous.alpha
import ambiguous.beta

fake.foo.do_something()
deep.mime.multipart.build()
lonely.only.run()
print(ambiguous)
