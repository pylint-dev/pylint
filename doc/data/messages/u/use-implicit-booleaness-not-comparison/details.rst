Following this check blindly in weakly typed code base can create hard to debug issues. If the value
can be something else that is falsey but not a sequence (for example ``None``, an empty string, or ``0``),
the code will not be equivalent.
