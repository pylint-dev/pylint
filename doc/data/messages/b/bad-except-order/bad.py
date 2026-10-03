try:
    print(int(input()))
except Exception:
    raise
except TypeError:  # [bad-except-order]
    # This block cannot be reached since TypeError exception
    # is caught by previous exception handler.
    raise
