"""inline loop non ascii variable definition"""
import os


test = [
    f"{łol}                                                                       "
    for łol in os.listdir(".")  # [non-ascii-name]
]
