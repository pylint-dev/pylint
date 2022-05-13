Removing ``[]`` inside calls that can use containers or generator indistinctly should be considered for performance reasons since a generator will have an upfront cost to pay. The performance will be better if
you are working with really long lists or sets and depending on the interpreter: you should consider
your dataset and your environment.

For ``max``, ``min`` and ``sum` using a generator is also best practices recommended by pep289.
