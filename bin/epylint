#!/usr/bin/env python

import re
import sys

from subprocess import *

p = Popen("pylint -f parseable -r n --disable-msg-cat=C,R %s" %
          sys.argv[1], shell = True, stdout = PIPE).stdout

for line in p:
    match = re.search("\\[([WE])(, (.+?))?\\]", line)
    if match:
        kind = match.group(1)
        func = match.group(3)

        if kind == "W":
           msg = "Warning"
        else:
           msg = "Error"

        if func:
            line = re.sub("\\[([WE])(, (.+?))?\\]",
                          "%s (%s):" % (msg, func), line)
        else:
            line = re.sub("\\[([WE])?\\]", "%s:" % msg, line)
    print line,

p.close()
