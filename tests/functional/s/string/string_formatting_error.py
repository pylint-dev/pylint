"""test string format error"""
# pylint: disable=unsupported-binary-operation,line-too-long,consider-using-f-string,too-few-public-methods

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
    print(f"{1:p}") # [bad-format-character]
    print("{:p}".format(1)) # [bad-format-character]
    print(f"{1:e} + {2:l}") # [bad-format-character]
    print("{:e} + {:l}".format(1, 1)) # [bad-format-character]
    print(f"{1:{2:q}}") # [bad-format-character]
    print("{:{:q}}".format(1, 2)) # [bad-format-character]


# Custom ``__format__`` accepting arbitrary spec text (cf. ``astropy.units``,
# ``astropy.units.Quantity``). The standard mini-format-spec parser doesn't
# recognise the spec, but the value's class consumes it, so no warning.
class _CustomFormat:
    def __format__(self, spec):
        return f"<{spec}>"

CUSTOM = _CustomFormat()
print(f"{CUSTOM:latex}")
print(f"{CUSTOM:cds}")
print(f"prefix [{CUSTOM:latex}] suffix")
print("{:cds}".format(CUSTOM))
# Mixed with a builtin format spec that's valid on its own.
print(f"{CUSTOM:cds} {1:d}")
# Whole-f-string silencing means a sibling int-with-bogus-spec is also
# silenced; this is a documented limitation of the coarse-grained check
# until per-FormattedValue spec parsing lands.
print(f"{CUSTOM:cds} {1:p}")
