def xor_check(*, left=None, right=None):
    if left is None != right is None:  # [bad-chained-comparison]
        raise ValueError('Either both left= and right= need to be provided or none should.')
