# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# Turn the '.. code-block:: lang' directives of a changelog into markdown fenced
# code blocks for the GitHub release notes, keeping their indentation in lists.
# The block ends at the first non-blank line indented like the directive, blank
# lines are held back so the closing fence stays next to the code.

c && /[^ ]/ && match($0, /^ */) && RLENGTH <= i { print p "```" b; c = 0; b = "" }
c && !/[^ ]/ { b = b "\n"; next }
c { printf "%s", b; b = ""; print p substr($0, i + 5); next }
match($0, /^ *\.\. code-block:: */) {
    i = index($0, ".") - 1
    p = substr($0, 1, i)
    print p "```" substr($0, RLENGTH + 1)
    c = 1
    getline  # the blank line after the directive
    next
}
{ print }
END { if (c) print p "```" }
