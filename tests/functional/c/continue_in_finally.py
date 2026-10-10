"""Test that `continue` is caught when met inside a `finally` clause."""

# pylint: disable=missing-docstring, lost-exception, broad-except

while True:
    try:
        pass
    finally:
        continue # [continue-in-finally]

while True:
    try:
        pass
    finally:
        break  # [break-in-finally]

while True:
    try:
        pass
    except Exception:
        pass
    else:
        continue


def nested_in_finally(items, lock):
    for item in items:
        try:
            pass
        finally:
            if item:
                continue  # [continue-in-finally]
            with lock:
                break  # [break-in-finally]


def nested_try_finally_in_finally(items):
    for _ in items:
        try:
            pass
        finally:
            try:
                pass
            finally:
                break  # [break-in-finally]


def loop_inside_finally(items):
    try:
        pass
    finally:
        for item in items:
            if item:
                continue
            break


def break_in_except_not_finally(items):
    for _ in items:
        try:
            pass
        except Exception:
            if items:
                break
        finally:
            pass
