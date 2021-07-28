""" Puts issue #2672 under test (-j 1 vs -j N)

Here we use a simple file to ensure configs are treated exactly the same way in -j 1 and
-j N """
import os  # pylint: disable=unused-import
