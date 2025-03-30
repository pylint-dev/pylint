# pylint: disable=missing-function-docstring, missing-module-docstring, line-too-long
# +1: [using-generic-type-syntax-in-unsupported-version, using-generic-type-syntax-in-unsupported-version]
type Point[T] = tuple[float, float]
# +1: [using-generic-type-syntax-in-unsupported-version, using-generic-type-syntax-in-unsupported-version]
type Alias[*Ts] = tuple[*Ts]
