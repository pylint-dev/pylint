"""
Simply variable test
"""
# pylint: disable=invalid-name

# Test invalid variable name
łol = "Foobar"  # [non-ascii-identifier]
# Usage should not raise a second error
łol += "-"  # [non-ascii-identifier]
