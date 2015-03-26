# pylint: disable=missing-docstring
from __future__ import print_function

def function(arg1, arg2, arg3, arg4, arg5): # [too-many-locals]
    arg6, arg7, arg8, arg9 = arg1, arg2, arg3, arg4
    print(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9)
    loc1, loc2, loc3, loc4, loc5, loc6, loc7 = arg1, arg2, arg3, arg4, arg5, \
 arg6, arg7
    print(loc1, loc2, loc3, loc4, loc5, loc6, loc7)
