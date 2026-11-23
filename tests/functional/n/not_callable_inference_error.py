# pylint: disable=missing-module-docstring,missing-function-docstring,invalid-name,unknown-option-value,undefined-variable,expression-not-assigned,used-before-assignment,consider-using-tuple
# Regression test for https://github.com/pylint-dev/pylint/issues/11492
# Previously pylint crashed (F0002 / astroid-error) when checking a call whose
# inferred class triggered an InferenceError during attribute lookup in
# TypeChecker.visit_call -> _check_uninferable_call. The crash is now guarded.

with _ as type.foo:
    pass


def fn():
    [C.foo() for _ in []]
    C = None
