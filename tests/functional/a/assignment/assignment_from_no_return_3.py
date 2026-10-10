"""Check 'known-side-effects-only-functions' hints in 'assignment-from-no-return'."""

# pylint: disable=invalid-name


def shuffle(sequence):
    """Shuffle the sequence in place, like 'random.shuffle' does."""
    sequence.reverse()


LST = [3, 2]
A = shuffle(LST)  # [assignment-from-no-return]
