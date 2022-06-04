"""Tests for the disabling of bad-option-value."""
# pylint: disable=invalid-name

# pylint: disable=bad-option-value

var = 1  # pylint: disable=a-removed-option

# pylint: enable=bad-option-value

var = 1  # pylint: disable=a-removed-option # [unknown-option-value]

# bad-option-value needs to be disabled before the bad option
var = 1  # pylint: disable=a-removed-option, bad-option-value # [unknown-option-value]
var = 1  # pylint: disable=bad-option-value, a-removed-option
