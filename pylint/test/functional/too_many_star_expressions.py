"""Test for too-many-star-expressions."""
# pylint: disable=unbalanced-tuple-unpacking
*FIRST, *SECOND = [1, 2, 3] # [too-many-star-expressions]
(FIRST, *SECOND), *THIRD = ((1, 2, 3), 4, 5)
*FIRST_1, SECOND = (1, 2, 3)
(*FIRST, *SECOND), THIRD = [...]  # [too-many-star-expressions]
((*FIRST, SECOND), *THIRD), *FOURTH = [...]
