"""simple pylint wrapper for emacs intraction"""

import re
import sys

from popen2 import popen3

def Run():
    p, _in, _err = popen3("pylint -f parseable -r n --disable-msg-cat=C,R,I %s"
                          % sys.argv[1])
    for line in p:
        match = re.search("\\[([WE])(, (.+?))?\\]", line)
        if match:
            if match.group(1) == "W":
                msg = "Warning"
            else:
                msg = "Error"
            func = match.group(3)
            if func:
                line = re.sub("\\[([WE])(, (.+?))?\\]",
                              "%s (%s):" % (msg, func), line)
            else:
                line = re.sub("\\[([WE])?\\]", "%s:" % msg, line)
        print line,
    p.close()
