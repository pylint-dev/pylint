"""Sibling dotted-submodule imports must be checked independently.

`import fake.bar` and `import fake.foo` both bind the local name `fake`, so
using one of them must not hide the other one being unused.

    https://github.com/pylint-dev/pylint/issues/2583
"""

# pylint: disable=missing-docstring, import-error

import fake.bar  # [unused-import]
import fake.foo

fake.foo.do_something()
