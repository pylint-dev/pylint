"""Test for *a = b """

*first = [1, 2, 3] # [invalid-star-assignment-target]
(*first, ) = [1, 2, 3]
