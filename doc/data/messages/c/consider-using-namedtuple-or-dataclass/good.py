from collections import namedtuple

MAPPING_1 = namedtuple("MAPPING_1", {"key_1", "key_2", "key_diff_1", "key_diff_2"})
entry_1 = {"key_1": 1, "key_2": 4, "key_diff_1": 4}
entry_2 = {"key_1": 1, "key_2": 4, "key_diff_2": 3}

MAPPING_1(1, 4, 4, 0)
MAPPING_1(1, 4, 0, 3)
