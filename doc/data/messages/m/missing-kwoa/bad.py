def target(pos, *, keyword):
    return pos + keyword


def not_forwarding_kwargs(*args, **kwargs):
    target(*args)  # [missing-kwoa]
