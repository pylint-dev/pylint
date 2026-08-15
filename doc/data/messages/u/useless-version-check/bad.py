import sys

if sys.version_info[:2] == (3, 5):  # [useless-version-check]
    PET = "dinosaur"
else:
    PET = "cat"
