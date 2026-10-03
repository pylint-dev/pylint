"""Functional test for consider-math-not-float."""

inf_float = float("inf")  # [consider-math-not-float]
neg_inf_float = float('-inf')  # [consider-math-not-float]
pos_inf_float = float("+inf")  # [consider-math-not-float]
infinity_float = float("infinity")  # [consider-math-not-float]
neg_infinity_float = float("-infinity")  # [consider-math-not-float]
large_exp_float = float("1e1000")
neg_large_exp_float = float("-1e1000")
very_large_exp_float = float("2.5E9999")
invalid_inf_float = float("in")  # [consider-math-not-float]
invalid_float_call = float("in", base=10)  # [consider-math-not-float]
nan_float = float("nan")  # [consider-math-not-float]
neg_nan_float = float("-nan")  # [consider-math-not-float]
pos_nan_float = float("+nan")  # [consider-math-not-float]
upper_nan_float = float("NaN")  # [consider-math-not-float]
typo_nan_float = float("nani")  # [consider-math-not-float]
other_typo_nan_float = float("nna")  # [consider-math-not-float]
