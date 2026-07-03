When a module has too many lines it can make it difficult to read and understand. There might be
performance issue while editing the file because the IDE must parse more code. You need more expertise
to navigate the file properly (go to a particular line when debugging, or search for a specific code construct, instead of navigating by clicking and scrolling)

This measure is a proxy for higher cyclomatic complexity that you might not be calculating if you're not using ``load-plugins=pylint.extensions.mccabe,``. Cyclomatic complexity is slower to compute, but also a more fine grained measure than raw SLOC. In particular, you can't make the code less readable by making a very complex one liner if you're using cyclomatic complexity.

The example simplify the code, but it's not always possible. Most of the time bursting the file
by creating a package with the same API is the only solution. Anticipating and creating the file
from the get go will permit to have the same end result with a better version control history.
