# pylint: disable=invalid-name
"""Checks for chained comparisons with comparisons belonging to different groups"""

primes = set(2, 3, 5, 7, 11)

def valid(x, y, z):
    """valid usage of chained comparisons"""
    if x < y <= z:
        pass
    elif x > y >= z:
        pass
    elif x == y != z:
        pass
    elif x is y is not z:
        pass
    elif x in y not in z:
        pass

def id_comparison_invalid(*, left=None, right=None):
    """identity mixed with comparison"""
    if left is None != right is None:  # [bad-chained-comparison]
        raise ValueError('Either both left= and right= need to be provided or none should.')
    if left is not None == right is not None:  # [bad-chained-comparison]
        pass

def member_comparison_invalid(x:int, y:int, z:int):
    """membership mixed with comparison"""
    if x in primes == y in primes:  # [bad-chained-comparison]
        pass
    elif x in primes == z not in primes:  # [bad-chained-comparison]
        pass
    elif x not in primes == y in primes != z not in primes:  # [bad-chained-comparison]
        pass
    elif x not in primes <= y not in primes > z in primes:  # [bad-chained-comparison]
        pass

def id_member_invalid(x:int, y:int, z:int):
    """identity mixed with membership"""
    if x in primes is y in primes:  # [bad-chained-comparison]
        pass
    elif x in primes is z not in primes:  # [bad-chained-comparison]
        pass
    elif x not in primes is y in primes is not z not in primes:  # [bad-chained-comparison]
        pass

def complex_invalid(x:int, y:int, z:int):
    """invalid complex chained comparisons"""
    if x in primes == y not in primes is not z in primes:  # [bad-chained-comparison]
        pass
    elif x < y <= z != x not in primes is y in primes:  # [bad-chained-comparison]
        pass
