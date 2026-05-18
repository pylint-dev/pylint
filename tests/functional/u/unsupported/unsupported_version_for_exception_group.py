# pylint: disable=missing-function-docstring, missing-module-docstring
def f():
    excs = [OSError("error 1"), SystemError("error 2")]
    # +1: [using-exception-groups-in-unsupported-version]
    raise ExceptionGroup("there were problems", excs)


try:  # [using-exception-groups-in-unsupported-version]
    f()
except* OSError as e:
    print("There were OSErrors")
except* SystemError as e:
    print("There were SystemErrors")


try:
    f()
except ExceptionGroup as group:  # [using-exception-groups-in-unsupported-version]
    # https://github.com/pylint-dev/pylint/issues/8985
    for exc in group.exceptions:  # pylint: disable=not-an-iterable
        print("ERROR: ", exc)
