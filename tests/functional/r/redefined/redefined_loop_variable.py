"cf. issue #8646 for context"
# pylint: disable=invalid-name
from collections import defaultdict
errors = [
    Exception("E101", "Boom!"),
    Exception("E101", "Bam!"),
    Exception("E102", "Shazam!"),
]
errors_per_arg0 = defaultdict(list)
for error in errors:
    errors_per_arg0[error.args[0]].append(error)
for arg0, errors in errors_per_arg0.items():  # [redefined-outer-name]
    print(arg0, "count:", len(errors))

pair = 2
for pair in errors_per_arg0.items():  # [redefined-outer-name]
    print(pair)

words = (
    ("A", ("a", "abandon", "ability", ...)),
    ("B", ("ball", "banana", ...)),
)
for letter, *words in words:  # [redefined-outer-name]
    print(letter, words)


#--- Notable cases where redefined-outer-name should NOT be raised:

# When the loop variable is re-assigned:
for i in enumerate(errors):
    i += 1

# When the same loop variables are used consecutively:
for k, v in errors_per_arg0.items():
    print(k, v)
for k, v in errors_per_arg0.items():
    print(k, v)
