def get_values(data):
    yield from data


for i in get_values(range(10)):
    pass
