"""Module with internal code duplication."""


def function_one(host, port, database):
    """First function with duplicated logic."""
    retries = 3
    timeout = 30
    connection_string = f"{host}:{port}/{database}"
    print(f"Connecting to {connection_string}")
    for attempt in range(retries):
        print(f"Attempt {attempt + 1} of {retries}")
        if attempt > 0:
            print(f"Waiting {timeout} seconds before retry")
    return connection_string


def unrelated():
    """Something completely different."""
    return 42


def function_two(host, port, database):
    """Second function with duplicated logic."""
    retries = 3
    timeout = 30
    connection_string = f"{host}:{port}/{database}"
    print(f"Connecting to {connection_string}")
    for attempt in range(retries):
        print(f"Attempt {attempt + 1} of {retries}")
        if attempt > 0:
            print(f"Waiting {timeout} seconds before retry")
    return connection_string
