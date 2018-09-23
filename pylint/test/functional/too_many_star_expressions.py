"""Test for too-many-star-expressions."""

*FIRST, *SECOND = [1, 2, 3] # [too-many-star-expressions]
(FIRST, *SECOND), *THIRD = ((1, 2, 3), 4, 5)
*FIRST_1, SECOND = (1, 2, 3)
