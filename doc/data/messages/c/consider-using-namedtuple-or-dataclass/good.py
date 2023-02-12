from collections import namedtuple

MAPPING_1 = namedtuple("MAPPING_1", {"key_1", "key_2", "key_diff_1", "key_diff_2"})
entry_1 = {"key_1": 0, "key_2": 1, "key_diff_1": 2}
entry_2 = {"key_1": 0, "key_2": 1, "key_diff_2": 3}

MAPPING_1(0, 1, 2, 0)
MAPPING_1(0, 1, 0, 3)
