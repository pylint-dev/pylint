"""Functional test for use-math-not-float."""

inf_float = float("inf")  # [use-math-not-float]
neg_inf_float = float('-inf')  # [use-math-not-float]
pos_inf_float = float("+inf")  # [use-math-not-float]
infinity_float = float("infinity")  # [use-math-not-float]
neg_infinity_float = float("-infinity")  # [use-math-not-float]
large_exp_float = float("1e1000")
neg_large_exp_float = float("-1e1000")
very_large_exp_float = float("2.5E9999")
invalid_inf_float = float("in")  # [use-math-not-float]
invalid_float_call = float("in", base=10)  # [use-math-not-float]
nan_float = float("nan")  # [use-math-not-float]
neg_nan_float = float("-nan")  # [use-math-not-float]
pos_nan_float = float("+nan")  # [use-math-not-float]
upper_nan_float = float("NaN")  # [use-math-not-float]
