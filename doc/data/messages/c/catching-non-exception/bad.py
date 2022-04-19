class FooError:
    pass


try:
    1 / 0
except FooError:  # [catching-non-exception]
    pass
