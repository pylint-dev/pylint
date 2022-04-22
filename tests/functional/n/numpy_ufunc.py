"""Test that pylint doesn't complain about numpy ufunc in % formatting"""
from numpy import radians, degrees #  any ufunc will do

a=radians(90.0)
print ( "%6.3f"%( degrees(a),)) # [consider-using-f-string]
print ( "%6.3f"% degrees(a)) # [consider-using-f-string]
print ( f"{degrees(a):6.3f}" )
