from pylint.checkers import BaseChecker
from pylint.interfaces import IRawChecker


def is_line_commented(line):
    """ Checks if a `# symbol that is not part of a string was found in line"""

    comment_idx = line.find(b"#")
    if comment_idx == -1:
        return False
    if comment_part_of_string(line, comment_idx):
        return is_line_commented(line[:comment_idx] + line[comment_idx + 1 :])
    return True


def comment_part_of_string(line, comment_idx):
    """ checks if the symbol at comment_idx is part of a string """

    if (
        line[:comment_idx].count(b"'") % 2 == 1
        and line[comment_idx:].count(b"'") % 2 == 1
    ) or (
        line[:comment_idx].count(b'"') % 2 == 1
        and line[comment_idx:].count(b'"') % 2 == 1
    ):
        return True
    return False


class CommentChecker(BaseChecker):
    __implements__ = IRawChecker

    name = "refactoring"
    msgs = {
        "R2044": (
            "Line with empty comment",
            "empty-comment",
            (
                "Used when a # symbol appears on a line not followed by an actual comment"
            ),
        )
    }
    options = ()
    priority = -1  # low priority

    def process_module(self, node):
        with node.stream() as stream:
            for (line_num, line) in enumerate(stream):
                line = line.rstrip()
                if line.endswith(b"#"):
                    if not is_line_commented(line[:-1]):
                        self.add_message("empty-comment", line=line_num + 1)


def register(linter):
    linter.register_checker(CommentChecker(linter))
