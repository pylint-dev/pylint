"""
Dummy test file to test the --minimal-messages-config option.

This file is tested in ``test_minimal_messages_config_enabled`` and
``test_minimal_messages_config_excluded_file``.
"""

f = open("foo.txt")  # [consider-using-with, unspecified-encoding]

print("%d" % 1)  # [consider-using-f-string]
