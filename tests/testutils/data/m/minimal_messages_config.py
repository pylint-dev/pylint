"""Dummy test file to test the --minimal-messages-config option."""

f = open("foo.txt")  # [consider-using-with, unspecified-encoding]

print("%d" % 1)  # [consider-using-f-string]
