By using a generator you can cut the execution tree and exit directly at the first element that is ``False`` for ``all`` or ``True`` for ``any`` instead of
calculating all the elements. Except in the worst possible case where you still need to evaluate everything (all values
are True for ``all`` or all values are false for ``any``) performance will be better.
