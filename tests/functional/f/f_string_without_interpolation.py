# pylint: disable=missing-module-docstring
import math

VALUE = 1

print(f"some value {VALUE}")
print(f'pi: {math.pi:.3f}')

print(f"ERROR")  # [f-string-without-interpolation]
