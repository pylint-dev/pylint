"""Names that redefine an import take part in the multiple naming style detection."""

try:
    from os.path import isfile as appleJuice
except ImportError:
    appleJuice = None

try:
    from os.path import isdir as bananaBread
except ImportError:
    bananaBread = None

red_fruit = 1  # [invalid-name]

print(appleJuice, bananaBread, red_fruit)
