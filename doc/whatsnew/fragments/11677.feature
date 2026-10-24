Add the ``ignore-local-names`` option to the similarities checker (``duplicate-code``).
When enabled, function-local names (arguments and assigned variables) are compared up
to a consistent renaming, so a copied block whose local variables were renamed is
still reported.

Closes #11677
