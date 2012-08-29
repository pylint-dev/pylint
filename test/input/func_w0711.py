"""find binary operations used as exceptions
"""

__revision__ = 1

try:
    __revision__ += 1
except Exception or StandardError:
    print "caught1"
except Exception and StandardError:
    print "caught2"
except (Exception or StandardError):
    print "caught3"
except (Exception or StandardError), exc:
    print "caught4"
