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
# A class object (not an instance) in the format field. At runtime this
# raises TypeError, but we don't flag it: a class can have an __init__ or
# be wrapped, so the inferred type is too uncertain to warn on.
print(f"{int:s}")
print(f"{int:invalid}")
# Same for the old ``%``-style: a tuple containing a class as the only
# argument should not be flagged.
print("%d" % (int,))


# A function parameter has no statically known type, so neither an invalid
# spec on it nor a builtin spec mismatch can be confirmed; both stay silent.
def fmt(x):
    """No warning: ``x`` is a parameter with no known type."""
    print(f"{x:invalid}")
    print(f"{x:d}")


# Every .format() argument kind (explicit positional, implicit positional,
# named) with a type mismatch must be flagged consistently.
print("{0:d}".format("abc"))  # [bad-string-format-type]
print("{:d}".format("abc"))  # [bad-string-format-type]
print("{name:d}".format(name="abc"))  # [bad-string-format-type]


# A spec containing ``%`` is treated as a strftime-style pattern: no warning
# is emitted, even if the value isn't a datetime. (Real datetimes work
# identically; an int stands in here because datetime.datetime.now() isn't
# statically inferable.)
print(f"{1:%d}")


# A class that defines __getattr__ may resolve any attribute name at
# runtime, so missing-format-attribute should not fire on ``{0.missing}``
# when the formatted value is an instance of such a class.
class _Dynamic:
    def __getattr__(self, name):
        return name

print("{0.missing}".format(_Dynamic()))
# A spec containing a nested ``{}`` (dynamic precision / width) is partly
# determined at runtime; no warning.
PREC = 3
print(f"{1.5:{PREC}f}")
# ``!r`` converts the value to its repr (a str) before the spec applies,
# so ``:s`` on any !r-converted value is valid.
print(f"{True!r:s}")
# Nested replacement field inside the spec: the outer spec is dynamic
# (skipped), while the inner ``{PREC}`` is itself just an int reference.
print(f"{1.5:.{PREC}f}")
