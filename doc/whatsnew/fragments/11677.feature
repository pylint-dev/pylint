Add the ``ignore-local-names`` option to the similarities checker (``duplicate-code``).
When enabled, function-local names (arguments and assigned variables) are compared up
to a consistent renaming, so a copied block whose local variables were renamed is
still reported.

Default arguments and the outermost iterable of a comprehension use their
enclosing scope. Type names in function annotations and names declared with
``global`` or ``nonlocal`` keep their spelling.

Closes #11677
