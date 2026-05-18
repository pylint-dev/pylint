"""inline loop non ascii variable definition"""
import os


TEST = [
    f"{łol}                                                                       "
    for łol in os.listdir(".")  # [non-ascii-name]
]
