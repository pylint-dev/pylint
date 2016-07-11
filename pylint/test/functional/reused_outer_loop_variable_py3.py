"""Python >= 3 tests for reused-outer-loop-variable."""

for i, *j in [(1, 2, 3, 4)]:
    for j in range(i): #[reused-outer-loop-variable]
        print(j)
