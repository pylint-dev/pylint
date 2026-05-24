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
# The custom-format carve-out is per-value, so a sibling int with a bogus
# spec is still flagged independently.
print(f"{CUSTOM:cds} {1:p}")  # [bad-format-character]


# F-string expressions can contain arbitrary Python syntax; the spec checker
# should not be confused by dict/set literals, comprehensions, nested
# f-strings, or PEP 701 same-quote nesting inside ``{...}``. None of these
# should be flagged.
from urllib.parse import urlencode  # pylint: disable=wrong-import-position

QUERY = "x"
URL = "/x"
# Dict literal inside an f-string expression.
print(f"{urlencode({'q': QUERY})}")
# Nested dict literals inside a function call.
print(f"```\n{ {'a': [{'b': 1}]} }\n```")
# Dict / set comprehensions inside an f-string expression.
ITEMS = {"a": 1, "b": 2}
print(f"approx({ ({k: v * 2 for k, v in ITEMS.items()})!r})")
print(f"set({ {x * 2 for x in [1, 2, 3]} })")
# Nested f-string inside an outer f-string's expression.
OFFSET = (1, 9)
SIZE = 100
print(f"bytes {f'{OFFSET[0]}-{OFFSET[1]}'}/{SIZE}")
# PEP 701 same-quote nesting requires Python 3.12+; see
# string_formatting_error_py312.py for that case.


# A non-PEP-3101 spec on a builtin type (which doesn't override __format__
# with a custom mini-language) fires bad-format-string.
print(f"{1:invalid}")  # [bad-format-string]
print("{:invalid}".format(1))  # [bad-format-string]
# A class object (not an instance) in the format field: at runtime this
# raises TypeError, but pylint conservatively returns True (don't flag) so
# user-defined formatters aren't tripped up.
print(f"{int:s}")
print(f"{int:invalid}")
# Same conservative behaviour for the old %-style when the inferred value is
# a class (not an Instance); the tuple form puts the class in the args list
# and exercises arg_matches_format_type's non-Instance fallback.
print("%d" % (int,))


# Function parameters infer to Uninferable; both the spec-parse error path
# (would emit bad-format-string) and the type-check path (would emit
# bad-string-format-type) should bail silently.
def fmt(x):
    """Exercises the Uninferable-arg branches in _node_has_custom_format
    and _check_formatted_value."""
    print(f"{x:invalid}")
    print(f"{x:d}")
# The dynamic-precision spec ``f"{x:{prec}f}"`` is partly dynamic; the
# spec-text walker bails out and emits nothing.
PREC = 3
print(f"{1.5:{PREC}f}")
# A bool with !r conversion is type-checked as str against the format
# character. ``!r`` of any value is a str so :s is fine.
print(f"{True!r:s}")
# Inner FormattedValue in spec (dynamic): no spec-text check; the inner
# value's own spec is checked when iterating nested FormattedValues.
print(f"{1.5:.{PREC}f}")
