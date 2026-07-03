FRUITS = {"apple": 1, "orange": 10}


def pick_fruit(name):
    try:  # [too-many-try-statements]
        count = FRUITS[name]
        count += 1
        print(f"Got fruit count {count}")
    except KeyError:
        return
