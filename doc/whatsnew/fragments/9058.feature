Do not report ``too-many-instance-attributes`` for a dataclass or NamedTuple
without public methods.
Fix a false negative where ``too-many-instance-attributes`` was not reported
for a NamedTuple.

Closes #9058
