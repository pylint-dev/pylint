"""used-before-assignment (E0601)"""
def function():
    """Assume except blocks execute if the try block returns."""
    try:
        return "success message"
    except ValueError:
        failure_message = "failure message"

    return failure_message
