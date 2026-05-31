"""Test deprecated modules using '__import__' builtin method."""
# pylint: disable=invalid-name

imp = __import__("mypackage")  # [deprecated-module]

imp_meth = __import__("mypackage").meth()  # [deprecated-module]

lib = "mypackage"
infer_imp = __import__(lib)  # [deprecated-module]

# Regression test for https://github.com/pylint-dev/pylint/issues/11059
# A non-string argument to ``__import__`` (caught by ``no-value-for-parameter``
# at runtime) should not crash the deprecated checker.
non_str = __import__(1)
