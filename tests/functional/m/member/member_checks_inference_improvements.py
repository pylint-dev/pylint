# pylint: disable=missing-docstring


def test_oserror_has_strerror():
    # https://github.com/PyCQA/pylint/issues/2553
    try:
        raise OSError()
    except OSError as exc:
        if exc.strerror is not None:
            return exc.strerror.lower()
        return None
