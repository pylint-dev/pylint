# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
from __future__ import annotations

MAX_GITHUB_COMMENT_LENGTH = 65536


def truncate_comment(
    comment: str, commit: str, max_length: int = MAX_GITHUB_COMMENT_LENGTH
) -> str:
    """Truncate a GitHub comment and append the generating commit."""
    hash_information = f"*This comment was generated for commit {commit}*"
    if len(comment) + len(hash_information) >= max_length:
        truncation_information = (
            f"*This comment was truncated because GitHub allows only"
            f" {max_length} characters in a comment.*"
        )
        # Reserve space for the ellipsis, the suffix and the potential
        # closing tags for a code fence and a <details> block.
        suffix = f"\n{truncation_information}\n\n"
        ellipsis = "\n...\n"
        code_fence = "```\n"
        closing_tag = "</details>\n"
        max_len = (
            max_length
            - len(hash_information)
            - len(suffix)
            - len(ellipsis)
            - len(code_fence)
            - len(closing_tag)
        )
        # Cut at the last line break before the limit so the comment ends
        # with complete lines (links and diff lines contain no space to
        # cut at); fall back to a hard cut inside a very long line.
        cut_point = comment.rfind("\n", 0, max_len)
        if cut_point <= 0:
            cut_point = max_len
        comment = comment[:cut_point] + ellipsis
        # Close any code fence or <details> tag left open by the cut.
        if comment.count("```") % 2:
            comment += code_fence
        if comment.count("<details>") > comment.count("</details>"):
            comment += closing_tag
        comment += suffix
    comment += hash_information
    return comment
