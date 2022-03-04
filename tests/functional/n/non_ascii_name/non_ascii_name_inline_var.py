"""inline loop non ascii variable definition"""
import os


foo = [
    f"{łol}                                                                       "
    for łol in os.listdir(".")  # [non-ascii-name]
]
