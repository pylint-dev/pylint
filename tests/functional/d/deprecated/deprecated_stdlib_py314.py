"""Test deprecations of the standard library added in Python 3.14."""
# pylint: disable=unused-import,invalid-name,too-few-public-methods

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
var.trace_remove("write", callback_name)

debugger = pdb.Pdb()
print(debugger.curframe_locals)  # [deprecated-attribute]
print(debugger.curframe.f_locals)


class MyDebugger(pdb.Pdb):
    """A derived debugger, as targeted by the 3.14 deprecation notice."""

    def show_locals(self):
        """Read, set and replace the deprecated frame locals."""
        print(self.curframe_locals)  # [deprecated-attribute]
        self.curframe_locals = {}  # [deprecated-attribute]
        print(self.curframe.f_locals)
