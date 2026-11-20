"""Generated callbacks can be called before the generator advances."""
# pylint: disable=missing-function-docstring,redefined-outer-name

callbacks = (lambda: print(index) for index in range(3))
for callback in callbacks:
    callback()


def consume_inline():
    for callback in (lambda: index for index in range(3)):
        print(callback())


def consume_with_filter():
    callbacks = (lambda: index for index in range(3) if index)
    for callback in callbacks:
        if callback():
            print(callback())


def store_callbacks():
    callbacks = (lambda: index for index in range(3))  # [cell-var-from-loop]
    saved = []
    for callback in callbacks:
        saved.append(callback)
    return saved


def defer_calls():
    callbacks = (lambda: index for index in range(3))  # [cell-var-from-loop]
    saved = []
    for callback in callbacks:
        saved.append(lambda: callback() + 1)  # [cell-var-from-loop]
    return saved


def store_generator_results():
    callbacks = (lambda: (yield index) for index in range(3))  # [cell-var-from-loop]
    saved = []
    for callback in callbacks:
        saved.append(callback())
    return saved


def store_returned_generators():
    callbacks = (lambda: (index for _ in range(1)) for index in range(3))  # [cell-var-from-loop]
    saved = []
    for callback in callbacks:
        saved.append(callback())
    return saved
