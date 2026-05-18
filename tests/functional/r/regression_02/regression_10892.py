# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/10892

Crash in ``_called_in_methods`` when ``klass.getattr()`` returns non-NodeNG
objects (e.g. ``UninferableBase``) from the metaclass lookup path.
"""

# pylint: disable=missing-docstring,too-few-public-methods,undefined-variable


class Meta(type):
    __init__ = some_descriptor


class MyClass(metaclass=Meta):
    def setup(self):
        self.attr = 1  # [attribute-defined-outside-init]

    def method(self):
        self.attr = 2  # [attribute-defined-outside-init]
