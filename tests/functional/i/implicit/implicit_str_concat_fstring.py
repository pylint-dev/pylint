# pylint: disable=invalid-name, missing-docstring, superfluous-parens, f-string-without-interpolation, pointless-statement
"""Implicit string concatenation involving f-strings (#8968)."""

a = 1
b = 2

raise_args = [f"{a} = " f"{b}."]  # [implicit-str-concat]
mixed_first = (f"{a}" "b", "c")  # [implicit-str-concat]
mixed_last = {"a", "b" f"{b}"}  # [implicit-str-concat]
print(f"{a} = " f"{b}.")  # [implicit-str-concat]
print("a", f"{a}" f"{b}")  # [implicit-str-concat]
assigned = f"{a}" f"{b}"  # [implicit-str-concat]
nested_quotes = [f"{f'{a}'}" f"{b}"]  # [implicit-str-concat]
non_ascii = ("Café", f"{a}" f"Café")  # [implicit-str-concat]

# A single f-string, or f-strings separated by a comma, is fine
single = f"{a}"
separated = [f"{a}", f"{b}"]
print(f"{a}")
print(f"{a}", f"{b}")
print(f"{a}" + f"{b}")

# Strings on different lines are only reported with check-str-concat-over-line-jumps
multiline = (f"{a}", f"{b}"
             f"{a}")

# Parenthesized single argument is fine
print(
    f"{a} = "
    f"{b}."
)

# Mixing a raw and a non-raw string cannot be a forgotten comma (#6663)
MIXED_RAW = [rf"\d{a}" "\n"]

# Statements on consecutive lines are not concatenated
first = f"{a}"
f"{b}"
