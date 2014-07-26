"""Warn about binary operations used as exceptions."""

try:
    pass
except Exception or StandardError:  # [binary-op-exception]
    print "caught1"
except Exception and StandardError:  # [binary-op-exception]
    print "caught2"
except Exception or StandardError:  # [binary-op-exception]
    print "caught3"
except (Exception or StandardError), exc:  # [binary-op-exception]
    print "caught4"
