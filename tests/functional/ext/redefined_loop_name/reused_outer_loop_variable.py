"""Tests for redefining an outer loop variable."""


# Simple nested loop
for i in range(10):
    for i in range(10): #[redefined-loop-name]
        print(i)

# When outer loop unpacks a tuple
for i, i_again in enumerate(range(10)):
    for i in range(10): #[redefined-loop-name]
        print(i, i_again)

# When inner loop unpacks a tuple
for i in range(10):
    for i, i_again in range(10): #[redefined-loop-name]
        print(i, i_again)

# With nested tuple unpacks
for (a, (b, c)) in [(1, (2, 3))]:
    for i, a in range(10): #[redefined-loop-name]
        print(i, a, b, c)

# Ignores when in else
for i in range(10):
    print(i)
    if i > 5:
        break
else:
    for i in range(2):
        print(i)

# Ignores dummy variables
for _ in range(10):
    for _ in range(10):
        print("Hello")

# Unpacking
for i, *j in [(1, 2, 3, 4)]:
    for j in range(i):  # [redefined-loop-name]
        print(j)
