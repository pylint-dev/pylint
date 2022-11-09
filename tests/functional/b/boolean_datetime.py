"""Test boolean-datetime

'py-version' needs to be set to <= '3.5'.
"""
import datetime

if datetime.time(0, 0, 0):  # [boolean-datetime]
    print("datetime.time(0,0,0) is not a bug!")
else:
    print("datetime.time(0,0,0) is a bug!")

if datetime.time(0, 0, 1):  # [boolean-datetime]
    print("datetime.time(0,0,1) is not a bug!")
else:
    print("datetime.time(0,0,1) is a bug!")
