def compare_apples(apples=20):
    for i in range(10):
        if 5 <= i:  # [misplaced-comparison-constant]
            pass
        if 1 == i:  # [misplaced-comparison-constant]
            pass
        if 20 < len(apples):  # [misplaced-comparison-constant]
            pass
