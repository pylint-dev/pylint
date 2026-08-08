"""Check that 'known-treacherous-functions' adds a hint to 'assignment-from-no-return'."""

# pylint: disable=invalid-name


def shuffle(sequence):
    """Shuffle the sequence in place, like 'random.shuffle' does."""
    sequence.reverse()


LST = [3, 2]
A = shuffle(LST)  # [assignment-from-no-return]
