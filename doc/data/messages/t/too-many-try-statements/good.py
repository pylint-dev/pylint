FRUITS = {"apple": 1, "orange": 10}


def pick_fruit(name):
    try:
        count = FRUITS[name]
    except KeyError:
        return

    count += 1
    print(f"Got fruit count {count}")
