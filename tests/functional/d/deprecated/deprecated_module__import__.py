"""Test deprecated modules using '__import__' builtin method."""
# pylint: disable=invalid-name

imp = __import__("mypackage")  # [deprecated-module]

imp_meth = __import__("mypackage").meth()  # [deprecated-module]

lib = "mypackage"
infer_imp = __import__(lib)  # [deprecated-module]
