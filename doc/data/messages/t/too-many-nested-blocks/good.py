def correct_fruits(fruits):
    if len(fruits) > 1 and "apple" in fruits and "orange" in fruits:
        count = fruits["orange"]
        if count % 2 and "kiwi" in fruits and count == 2:
            return True
    return False
