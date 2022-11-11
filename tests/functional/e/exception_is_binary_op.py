"""Warn about binary operations used as exceptions."""

try:
    pass
except Exception or BaseException:  # [binary-op-exception]
    print("caught1")
except Exception and BaseException:  # [binary-op-exception]
    print("caught2")
except Exception or BaseException:  # [binary-op-exception]
    print("caught3")
except (Exception or BaseException) as exc:  # [binary-op-exception]
    print("caught4")
