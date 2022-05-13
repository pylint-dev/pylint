Removing ``[]`` inside calls that can use containers or generators should be considered
for performance reasons since a generator will have an upfront cost to pay. The
performance will be better if you are working with long lists or sets.

For ``max``, ``min`` and ``sum`` using a generator is also recommended by pep289.
