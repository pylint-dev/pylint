# +1: [missing-format-string-key]
fruit_prices = """
Apple: %(apple_price)d ¤
Orange: %(orange_price)d ¤
""" % {
    "apple_price": 42
}
