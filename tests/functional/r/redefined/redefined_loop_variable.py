"cf. issue #8646 for context"
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
print(errors)
