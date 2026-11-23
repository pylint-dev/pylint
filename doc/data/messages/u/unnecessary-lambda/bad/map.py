fruits = ["banana", "kiwi", "apple"]
by_length = sorted(fruits, key=lambda fruit: len(fruit))  # [unnecessary-lambda]
