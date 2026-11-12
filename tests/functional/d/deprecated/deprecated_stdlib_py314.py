"""Test deprecations of the standard library added in Python 3.14."""
# pylint: disable=unused-import,invalid-name

import nturl2path  # [deprecated-module]
import pdb
import tkinter

var = tkinter.StringVar()
callback_name = var.trace_variable("w", print)  # [deprecated-method]
var.trace("w", print)  # [deprecated-method]
var.trace_vinfo()  # [deprecated-method]
var.trace_vdelete("w", callback_name)  # [deprecated-method]
var.trace_add("write", print)
var.trace_info()

debugger = pdb.Pdb()
print(debugger.curframe_locals)  # [deprecated-attribute]
print(debugger.curframe)
