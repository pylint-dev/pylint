Following this check blindly in weakly typed code base can create hard to debug issues. If the value
can be something else that is falsey but not an ``int`` (for example ``None``, or an empty string),
the code will not be equivalent.
