# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/10422

f-string getattr should be treated like %%-format for not-callable.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

# pylint: disable=missing-docstring,too-few-public-methods
class MyClass:
    meth_name = "test"

    def _call_test(self):
        pass

    def _call_provider(self):
        method = getattr(self, f"_call_{self.meth_name}", None)
        method()
        method2 = getattr(self, "_call_%s" % self.meth_name, None)
        method2()
