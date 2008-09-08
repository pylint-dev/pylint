@echo off
rem = """-*-Python-*- script
@echo off
rem -------------------- DOS section --------------------
rem You could set PYTHONPATH or TK environment variables here
python -x %~f0 %*
goto exit
 
"""
# -------------------- Python section --------------------
import sys
from pylint.checkers import similar
similar.run()
 

DosExitLabel = """
:exit
rem """


