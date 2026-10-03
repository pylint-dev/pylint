"""Regression test."""
def crash_on_unary_op_with_name():
    """Should not crash with -idx."""
    mylist = []
    idx = 5
    for _i, _val in enumerate(mylist, start=-idx):
        pass
