"""Tests for star-arg-unpacking-after-keyword-arg."""


def func(*args, **kwargs):
    """Accept anything."""
    return args, kwargs


ARGS = (1,)
OTHER = (2,)
KWARGS = {"z": 3}

func(y=2, *ARGS)  # [star-arg-unpacking-after-keyword-arg]
func(1, y=2, *ARGS)  # [star-arg-unpacking-after-keyword-arg]
func(*ARGS, y=2, *OTHER)  # [star-arg-unpacking-after-keyword-arg]
func(
    y=2,
    *ARGS,  # [star-arg-unpacking-after-keyword-arg]
)

func(y=2, *ARGS, **KWARGS)  # [star-arg-unpacking-after-keyword-arg]

func(*ARGS, y=2)
func(*ARGS, y=2, **KWARGS)
func(*ARGS, **KWARGS)
func(y=2, **KWARGS)
func(1, *ARGS)
func(1, y=2)
