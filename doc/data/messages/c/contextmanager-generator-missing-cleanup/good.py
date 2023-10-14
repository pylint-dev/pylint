import contextlib


@contextlib.contextmanager
def good_cm_except():
    print("good cm enter")
    try:
        a = yield
    except GeneratorExit:
        print("good cm exit")
