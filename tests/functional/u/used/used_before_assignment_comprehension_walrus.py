"""A name bound by a walrus in the ``if`` of a comprehension is usable in the parts
evaluated afterwards. Regression test for https://github.com/pylint-dev/pylint/issues/9460
"""


def service_or_none(port: int) -> str | None:
    """Return a service name for some ports."""
    return f"service-{port}" if port % 2 else None


KNOWN_SERVICES = [
    service for port in range(1, 1024) if
    (service := service_or_none(port))
]
KNOWN_PORTS = {
    service: port for port in range(1, 1024) if (service := service_or_none(port))
}
LENGTHS = {len(service) for port in range(1, 1024) if (service := service_or_none(port))}
UPPER = (service.upper() for port in range(1, 1024) if (service := service_or_none(port)))

# A later clause of the same comprehension...
CHARS = [
    (service, char)
    for port in range(1, 1024)
    if (service := service_or_none(port))
    for char in service
]
# ...or a later condition of the same clause can use the name too
LONG = [
    service
    for port in range(1, 1024)
    if (service := service_or_none(port))
    if len(service) > 9
]

# A condition evaluated before the one binding the name cannot
EARLY = [
    port
    for port in range(1, 1024)
    if early  # [used-before-assignment]
    if (early := service_or_none(port))
]


def in_function():
    """The same, in a function scope."""
    return [name for port in range(1, 1024) if (name := service_or_none(port))]
