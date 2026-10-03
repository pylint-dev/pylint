# pylint: disable=missing-docstring,unused-variable,line-too-long


# PEP 695 type parameters live in the function's locals but are type-system
# constructs, not runtime local variables, so they must not be counted towards
# ``too-many-locals``. This function has 16 type parameters but only one real
# local variable, so it must NOT emit ``too-many-locals``.
def build[T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16](arg):
    result = arg
    return result


# Mixed case: 16 type parameters plus 16 genuine local variables. Only the real
# locals are counted, so this emits ``too-many-locals`` at 16/15 (not 32/15).
def mixed[T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, T13, T14, T15, T16](start):  # [too-many-locals]
    loc0 = start
    loc1 = loc0 * 1
    loc2 = loc1 * 2
    loc3 = loc2 * 3
    loc4 = loc3 * 4
    loc5 = loc4 * 5
    loc6 = loc5 * 6
    loc7 = loc6 * 7
    loc8 = loc7 * 8
    loc9 = loc8 * 9
    loc10 = loc9 * 10
    loc11 = loc10 * 11
    loc12 = loc11 * 12
    loc13 = loc12 * 13
    loc14 = loc13 * 14
    return loc14
