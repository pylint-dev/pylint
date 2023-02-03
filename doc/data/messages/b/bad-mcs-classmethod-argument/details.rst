Used when a metaclass class method has a first argument named differently
than the value specified in valid-metaclass-classmethod-first-arg option
(default to `cls`), recommended to easily differentiate them from regular
instance methods.

Weird enough but usually naming of the first argument is `mcs` and pylint
documentation says so but when someone specifies it then the lib throws
C0204 error.
