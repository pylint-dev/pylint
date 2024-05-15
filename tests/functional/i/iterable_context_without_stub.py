"""If .pyi stubs are NOT preferred, no diagnostics emitted."""
import more_itertools

for val in more_itertools.chunked([1, 2, 3], n=1):
    print(val)
