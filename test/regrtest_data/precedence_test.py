"""
  # package/__init__.py
  class AudioTime(object):
    DECIMAL = 3

  # package/AudioTime.py
  class AudioTime(object):
    pass

  # test.py
  from package import AudioTime
  # E0611 - No name 'DECIMAL' in module 'AudioTime.AudioTime'
  print AudioTime.DECIMAL

"""

__revision__ = 0

from package import AudioTime

print AudioTime.DECIMAL
