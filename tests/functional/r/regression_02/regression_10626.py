""" Test case for issue #10626: nested builtins.min / builtins.max calls"""

import builtins

builtins.min(1, min(2, 3))  # [nested-min-max]
min(1, builtins.min(2, 3)) # [nested-min-max]
builtins.min(1, builtins.min(2, 3))  # [nested-min-max]

builtins.max(1, max(2, 3)) # [nested-min-max]
max(1, builtins.max(2, 3)) # [nested-min-max]
builtins.max(1, builtins.max(2, 3)) # [nested-min-max]
