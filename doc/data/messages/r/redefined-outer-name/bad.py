count = 10


def count_it(count):  # [redefined-outer-name]
    for i in range(count):
        print(i)


for count in range(10):  # [redefined-outer-name]
    print(count)
