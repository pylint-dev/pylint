"""test string format error"""
# pylint: disable=unsupported-binary-operation,line-too-long, consider-using-f-string

PARG_1 = PARG_2 = PARG_3 = 1


def pprint():
    """Test string format"""
    print("%s %s" % {'PARG_1': 1, 'PARG_2': 2})  # [too-few-format-args]
    print("%s" % (PARG_1, PARG_2))  # [too-many-format-args]
    print("%(PARG_1)d %d" % {'PARG_1': 1, 'PARG_2': 2})  # [mixed-format-string]
    print("%(PARG_1)d %(PARG_2)d" % {'PARG_1': 1})  # [missing-format-string-key]
    print("%(PARG_1)d %(PARG_2)d" % {'PARG_1': 1, 'PARG_2':2, 'PARG_3':3})  # [unused-format-string-key]
    print("%(PARG_1)d %(PARG_2)d" % {'PARG_1': 1, 2:3}) # [missing-format-string-key,bad-format-string-key]
    print("%(PARG_1)d %(PARG_2)d" % (2, 3)) # [format-needs-mapping]
    print("%(PARG_1)d %(PARG_2)d" % [2, 3]) # [format-needs-mapping]
    print("%2z" % PARG_1)  # [bad-format-character]
    print("strange format %2" % PARG_2) # [truncated-format-string]
    print("works in 3 %a" % 1)
    print("String" % PARG_1) # [format-string-without-interpolation]
    print("String" % ())  # [format-string-without-interpolation]
    print("String" % [])  # [format-string-without-interpolation]
    print("String" % None)  # [format-string-without-interpolation]
