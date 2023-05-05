"redefined-outer-name with loop variables - cf. issue #8646 for context"
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

# When loop variables are re-assigned:
for i, err in enumerate(errors):
    i += 1
    err = None

# When the same loop variables are used consecutively:
for k, v in errors_per_arg0.items():
    print(k, v)
for k, v in errors_per_arg0.items():
    print(k, v)

# When a similarly named loop variable is assigned in another loop (trickier to implement):
for n in range(10):
    n += 1
for n in range(10):
    n += 1
