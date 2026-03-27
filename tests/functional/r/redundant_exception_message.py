# pylint: disable=missing-docstring, broad-exception-caught, undefined-variable
# pylint: disable=raise-missing-from, line-too-long, invalid-name


class ConfigError(Exception):
    """Custom exception for configuration errors."""


# ===== BAD CASES (should trigger redundant-exception-message) =====

# f-string with direct exception reference
try:
    1 / 0
except ZeroDivisionError as err:
    raise ConfigError(f"Failed to save config: {err}") from err  # [redundant-exception-message]

# f-string with str(err)
try:
    1 / 0
except ZeroDivisionError as err:
    raise ConfigError(f"Failed to save config: {str(err)}") from err  # [redundant-exception-message]

# String concatenation with str(err)
try:
    1 / 0
except ZeroDivisionError as err:
    raise ConfigError("Failed to save config: " + str(err)) from err  # [redundant-exception-message]

# str(err) as sole argument
try:
    1 / 0
except ZeroDivisionError as err:
    raise ConfigError(str(err)) from err  # [redundant-exception-message]

# Direct exception reference as argument
try:
    1 / 0
except ZeroDivisionError as err:
    raise ConfigError(err) from err  # [redundant-exception-message]

# Nested concatenation
try:
    1 / 0
except ZeroDivisionError as err:
    raise ConfigError("Error: " + "details: " + str(err)) from err  # [redundant-exception-message]


# ===== GOOD CASES (should NOT trigger redundant-exception-message) =====

# Simple message without exception reference
try:
    1 / 0
except ZeroDivisionError as err:
    raise ConfigError("Failed to save configuration") from err

# Message with specific context (not the exception itself)
try:
    1 / 0
except ZeroDivisionError as err:
    path = "/path/to/config"
    raise ConfigError(f"Config file not found: {path}") from err

# f-string with different variable
try:
    1 / 0
except ZeroDivisionError as err:
    context = "user settings"
    raise ConfigError(f"Failed to save {context}") from err

# raise without from (separate rule: raise-missing-from)
try:
    1 / 0
except ZeroDivisionError as err:
    raise ConfigError(f"Failed: {err}")

# raise from None (explicit suppression of context)
try:
    1 / 0
except ZeroDivisionError as err:
    raise ConfigError("Failed to save config") from None

# No arguments to exception
try:
    1 / 0
except ZeroDivisionError as err:
    raise ConfigError from err

# Different exception variable in from clause
try:
    1 / 0
except ZeroDivisionError as err:
    other_err = ValueError("other")
    raise ConfigError(f"Error: {err}") from other_err
