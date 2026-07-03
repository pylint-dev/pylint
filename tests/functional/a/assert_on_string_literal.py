# pylint: disable=missing-module-docstring, undefined-variable
assert [foo, bar], "No AssertionError"
assert "There is an AssertionError" # [assert-on-string-literal]
assert "" # [assert-on-string-literal]
