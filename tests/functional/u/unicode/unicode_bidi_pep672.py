"""
Example of trojan unicode, see https://trojansource.codes/
This example was taken from PEP672
"""
# pylint: disable=invalid-name

# +1: [bidirectional-unicode]
example = "x‏" * 100  #    "‏x" is assigned
