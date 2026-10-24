"""The test of a conditional expression is evaluated before either branch.

So a branch can use a name assigned by a walrus in the test, even when the
conditional expression is nested in a larger expression.
https://github.com/pylint-dev/pylint/issues/7538
"""
# pylint: disable=missing-function-docstring, invalid-name, unused-variable

print("d" + (f"{s1}" if (s1 := "x") else ""))
print((f"{s2}" if (s2 := "x") else "") + "d")
print(f"{s3}" if (s3 := "x") else "")


def nested_in_expressions(value):
    concatenated = "d" + (first if (first := value) else "")
    negated = -(second if (second := len(value)) else 0)
    in_dict = {"k": "d" + (third if (third := value) else "")}
    in_list = ["d" + (fourth if (fourth := value) else "")]
    return concatenated, negated, in_dict, in_list


def used_in_else_branch(value):
    return "d" + ("" if (first := value) else first)


def walrus_nested_in_test(value):
    return "d" + (first if ((first := value) is not None) else "")


def used_in_nested_if_exp(value, flag):
    return "d" + (("x" if flag else first) if (first := value) else "")


def used_in_generator(value):
    return "d" + ("".join(first for _ in "ab") if (first := value) else "")


def other_statements(value):
    if "d" + (first if (first := value) else ""):
        pass
    assert "d" + (second if (second := value) else "")
    total = 1
    total += third if (third := len(value)) else 0
    return total


def read_in_test_before_walrus(value):
    return "d" + (first if (first + (first := value)) else "")  # [used-before-assignment]


def walrus_in_other_if_exp(value, flag):
    return "d" + (first if flag else ("x" if (first := value) else ""))  # [used-before-assignment]
