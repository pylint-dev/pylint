The `use-implicit-booleaness-not-comparison`, `use-implicit-booleaness-not-comparison-to-string`,
and `use-implicit-booleaness-not-comparison-to-zero` checks now distinguish between comparisons
used in boolean contexts and those that are not, enabling them to provide more accurate refactoring suggestions.

Closes #9353
