"""Test returns from structural pattern matching cases."""

def unpack(num) -> tuple[int, int]:
    """Return a tuple of integers."""
    match num:
        case 1:
            return 1, 1
        case _:
            return 0, 0

x, y = unpack(1)
