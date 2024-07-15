# pylint: disable=missing-function-docstring, missing-module-docstring, line-too-long
type Vector = list[float]  # [using-generic-type-syntax-in-unsupported-version]
# +1: [using-generic-type-syntax-in-unsupported-version, using-generic-type-syntax-in-unsupported-version]
type Alias[*Ts] = tuple[*Ts]
