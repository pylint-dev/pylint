@echo off
rem = """-*-Python-*- script
rem -------------------- DOS section --------------------
rem You could set PYTHONPATH or TK environment variables here
python -x "%~f0" %*
goto exit
 
"""
# -------------------- Python section --------------------
import sys
from pylint import lint
lint.Run(sys.argv[1:])
 

DosExitLabel = """
:exit
rem """


