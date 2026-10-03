class FooError(Exception):
    pass


try:
    1 / 0
except FooError:
    pass
