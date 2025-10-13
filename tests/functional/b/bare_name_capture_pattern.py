"""Functional tests for the ``bare-name-capture-pattern`` message"""


a = "a"
b = "b"
s = "a"


match s:
    case a:  # [bare-name-capture-pattern]
        pass
    case b:  # [bare-name-capture-pattern]
        pass
    case c if c == "Hello":
        pass
    case "a" as some_name:
        pass
    case s:
        pass
