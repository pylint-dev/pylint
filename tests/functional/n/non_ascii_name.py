""" Tests for non-ascii-name checker. """

áéíóú = {}.keys() # [non-ascii-name]
áéíóú = 4444 # [non-ascii-name]

def úóíéá(): # [non-ascii-name]
    """yo"""
