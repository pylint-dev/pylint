"""hum E1011 on .prec member is justifiable since Context instance are built
using setattr/locals :(
"""
import decimal

decimal.getcontext().prec = 200
print decimal.getcontext().prec

