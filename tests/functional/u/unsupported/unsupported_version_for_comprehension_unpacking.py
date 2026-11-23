"""Test that PEP 798 unpacking is reported when py-version is lower than 3.15."""
baskets = [["apple", "banana"], ["cherry"]]
stocks = [{"apple": 2}, {"cherry": 5}]

# +1: [using-comprehension-unpacking-in-unsupported-version]
fruits = [*basket for basket in baskets]
# +1: [using-comprehension-unpacking-in-unsupported-version]
unique = {*basket for basket in baskets}
# +1: [using-comprehension-unpacking-in-unsupported-version]
generated = (*basket for basket in baskets)
# +1: [using-comprehension-unpacking-in-unsupported-version]
merged = {**stock for stock in stocks}

# A comprehension that does not unpack its element is fine on every version.
flattened = [fruit for basket in baskets for fruit in basket]
counts = {fruit: 1 for fruit in flattened}
