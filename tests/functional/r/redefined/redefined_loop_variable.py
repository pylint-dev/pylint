"redefined-outer-name with loop variables - cf. issue #8646 for context"
# pylint: disable=global-statement,invalid-name,missing-function-docstring
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

def func0(*args, **kwargs):
    print(args, kwargs)
    for args in range(10):  # [redefined-outer-name]
        pass
    for _, kwargs in {}.items():  # [redefined-outer-name]
        pass


#--- Notable cases where redefined-outer-name should NOT be raised:

# When a dummy variable is used:
_ = 42
for _ in range(10):
    pass

# When loop variables are re-assigned:
for i, err in enumerate(errors):
    i += 1
    err = None

# When the same loop variables are used consecutively:
for k, v in errors_per_arg0.items():
    print(k, v)
for k, v in errors_per_arg0.items():
    print(k, v)

# When a similarly named loop variable is assigned in another loop:
for n in range(10):
    n += 1
for n in range(10):
    n += 1

# When the loop variable is re-assigned AFTER the for loop:
def func1():
    for value in range(10):
        print(value)
    if 1 + 1:
        value = 42

# When the variable is global or nonlocal:
glob = 42
def func2():
    global glob
    for glob in range(10):
        pass

# When the variable was just type-declared before the loop:
var: int
for var in (1, 2):
    print(var)

# Function argument override, already covered by redefined-argument-from-local:
def func3(arg):
    print(arg)
    for arg in range(10):  # [redefined-argument-from-local]
        pass
