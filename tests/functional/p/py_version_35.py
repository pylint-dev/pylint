"""No warnings should be emitted for features that require Python > 3.5"""
# pylint: disable=invalid-name

# consider-using-f-string -> requires Python 3.6
"Hello {}".format("World")
