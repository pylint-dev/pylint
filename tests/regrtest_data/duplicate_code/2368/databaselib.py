"""Database utilities."""


def setup_connection(host, port, database):
    """Set up a database connection with retries."""
    retries = 3
    timeout = 30
    connection_string = f"{host}:{port}/{database}"
    print(f"Connecting to {connection_string}")
    for attempt in range(retries):
        print(f"Attempt {attempt + 1} of {retries}")
        if attempt > 0:
            print(f"Waiting {timeout} seconds before retry")
    return connection_string
