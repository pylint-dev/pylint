"""Tests for used-before-assignment with assignments in except handlers after
try blocks with return statements.
See: https://github.com/PyCQA/pylint/issues/5500.
"""
def function():
    """Assume except blocks execute if the try block returns."""
    try:
        success_message = "success message"
        return success_message
    except ValueError:
        failure_message = "failure message"
    finally:
        print(failure_message)  # [used-before-assignment]

    return failure_message
