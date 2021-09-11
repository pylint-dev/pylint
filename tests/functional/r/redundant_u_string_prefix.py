""""Checks for redundant u-prefixes for strings"""
# pylint: disable=missing-function-docstring

def print_good():
    print("String")
    print(f"String{1 + 1}")


def print_bad():
    print(u"String")  # [redundant-u-string-prefix]
    print(u'String')  # [redundant-u-string-prefix]
    print([u"String", u"String2"])  # [redundant-u-string-prefix, redundant-u-string-prefix]
    print((u"String", u"String2"))  # [redundant-u-string-prefix, redundant-u-string-prefix]
    print({1: u"String"})  # [redundant-u-string-prefix]
