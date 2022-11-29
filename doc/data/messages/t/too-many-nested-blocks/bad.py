def correct_fruits(fruits):
    if len(fruits) > 1:  # [too-many-nested-blocks]
        if "apple" in fruits:
            if "orange" in fruits:
                count = fruits["orange"]
                if count % 2:
                    if "kiwi" in fruits:
                        if count == 2:
                            return True
    return False
