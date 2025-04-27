Enhanced W0236 (invalid-overridden-method) to detect return type mismatches in overridden methods.

Before this fix, Pylint did not catch return type mismatches when a method in a subclass overrode a method from a base class with a different return type. Now, Pylint will properly flag such mismatches, making the tool more consistent with type checkers like Pyright/Pylance.

Closes #10351
