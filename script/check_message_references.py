#!/usr/bin/env python3
# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Pre-commit hook to check and fix pylint message references in documentation.

This script scans documentation files for words containing dashes (like "no-member")
and converts them to Sphinx references (`:ref:`no-member``) if they are valid
pylint message symbols.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from re import Pattern

# Try to import pylint components
try:
    from pylint.checkers import initialize as initialize_checkers
    from pylint.extensions import initialize as initialize_extensions
    from pylint.lint.pylinter import PyLinter
except ImportError:
    print("Error: This script must be run in an environment where pylint is installed.")
    sys.exit(1)


class MessageReferenceChecker:
    """Checks and fixes pylint message references in documentation files."""

    # Pattern to find words with dashes that might be message symbols
    # Negative lookbehind/lookahead to avoid matching already formatted refs
    DASH_WORD_PATTERN: Pattern[str] = re.compile(
        r"(?<!:ref:`)"  # Not preceded by :ref:`
        r"(?<!`)(?<![/\\])"  # Not preceded by backtick or path separator
        r"\b([a-z]+(?:-[a-z]+)+)\b"  # Word with dashes (lowercase)
        r"(?!`)"  # Not followed by backtick
        r"(?![^\s]*\.(?:py|rst|md|txt|toml|yaml|yml|cfg|ini|json))"  # Not part of filename
    )

    # Pattern to check if already a proper reference
    REF_PATTERN: Pattern[str] = re.compile(r":ref:`([^`]+)`")

    # Pattern to detect code blocks in different formats
    CODE_BLOCK_PATTERNS = [
        # RST code blocks
        re.compile(r"^\.\. code-block::", re.MULTILINE),
        re.compile(r"^::\s*$", re.MULTILINE),
        # Markdown code blocks
        re.compile(r"^```", re.MULTILINE),
        re.compile(r"^~~~", re.MULTILINE),
        # Inline code
        re.compile(r"``[^`]+``"),  # RST inline
        re.compile(r"`[^`]+`"),  # Markdown inline (single backtick)
    ]

    # File extensions to check
    VALID_EXTENSIONS = {".md", ".rst", ".py", ".txt"}

    def __init__(self, verbose: bool = False, fix: bool = False):
        """Initialize the checker.

        Args:
            verbose: Whether to print verbose output
            fix: Whether to fix issues automatically
        """
        self.verbose = verbose
        self.fix = fix
        self.message_symbols = self._load_message_symbols()
        self.issues_found = 0
        self.files_fixed = 0

    def _load_message_symbols(self) -> set[str]:
        """Load all valid pylint message symbols."""
        linter = PyLinter()
        initialize_checkers(linter)
        initialize_extensions(linter)

        symbols = set()
        for message in linter.msgs_store.messages:
            symbols.add(message.symbol)
            # Also add old names if they exist
            if hasattr(message, "old_names"):
                for _, old_symbol in message.old_names:
                    symbols.add(old_symbol)

        if self.verbose:
            print(f"Loaded {len(symbols)} message symbols")

        return symbols

    def _is_in_code_block(self, content: str, match_start: int) -> bool:
        """Check if a match position is inside a code block.

        Args:
            content: The full file content
            match_start: The start position of the match

        Returns:
            True if the match is inside a code block
        """
        # Get the content before the match
        before_match = content[:match_start]

        # Check for RST code blocks
        if ".. code-block::" in before_match or "\n::" in before_match:
            # Simple heuristic: count indentation changes after last code block start
            lines_before = before_match.split("\n")
            for i in range(len(lines_before) - 1, -1, -1):
                line = lines_before[i]
                if ".. code-block::" in line or (line.strip() == "::"):
                    # We're likely in a code block if we haven't seen a dedent
                    return True
                if line and not line[0].isspace() and line.strip():
                    # Found a non-indented line, probably out of code block
                    break

        # Check for Markdown code fences
        fence_count = before_match.count("```") + before_match.count("~~~")
        if fence_count % 2 == 1:  # Odd number means we're inside a fence
            return True

        # Check if we're in inline code
        line_start = before_match.rfind("\n") + 1
        line_end = content.find("\n", match_start)
        if line_end == -1:
            line_end = len(content)
        current_line = content[line_start:line_end]

        # Check for inline code patterns
        rel_pos = match_start - line_start
        for pattern in ("``", "`"):
            parts = current_line.split(pattern)
            current_pos = 0
            in_code = False
            for i, part in enumerate(parts):
                if i > 0:
                    in_code = not in_code
                if current_pos <= rel_pos < current_pos + len(part):
                    return in_code
                current_pos += len(part) + len(pattern)

        return False

    def _should_skip_match(
        self, content: str, match: re.Match[str], filepath: Path
    ) -> bool:
        """Determine if a match should be skipped.

        Args:
            content: The full file content
            match: The regex match object
            filepath: Path to the file being checked

        Returns:
            True if the match should be skipped
        """
        # pylint: disable=too-many-locals
        word = match.group(1)
        start = match.start()

        # Skip if not a valid message symbol
        if word not in self.message_symbols:
            return True

        # Skip if already properly formatted
        # Check the surrounding context
        context_start = max(0, start - 10)
        context_end = min(len(content), match.end() + 10)
        context = content[context_start:context_end]
        if ":ref:`" in context and "`" in context:
            return True

        # Skip if in a code block
        if self._is_in_code_block(content, start):
            return True

        # Skip if it looks like a command-line argument (preceded by -- or -)
        before_start = max(0, start - 3)
        before = content[before_start:start]
        if "--" in before or (before and before[-1] == "-"):
            return True

        # Get the current line for context-specific checks
        line_start = content.rfind("\n", 0, start) + 1
        line_end = content.find("\n", start)
        if line_end == -1:
            line_end = len(content)
        line = content[line_start:line_end]
        word_pos_in_line = start - line_start

        # Skip if this is a pylint functional test comment
        # Pattern: # [message-name] or # [message-name, other-message]
        if "#" in line:
            comment_start = line.find("#")
            if 0 <= comment_start < word_pos_in_line:
                comment_part = line[comment_start:]
                # Check for [message-name] pattern in comments
                if "[" in comment_part and "]" in comment_part:
                    bracket_start = comment_part.find("[")
                    bracket_end = comment_part.find("]")
                    if bracket_start < bracket_end:
                        # Check if our word is inside the brackets
                        word_rel_pos = word_pos_in_line - comment_start
                        if bracket_start < word_rel_pos < bracket_end:
                            return True

        # Skip if in a functional test file path
        if "functional" in str(filepath) or "test" in str(filepath):
            # In test files, be extra conservative about comments
            if "#" in line and line.find("#") < word_pos_in_line:
                return True

        # Skip if part of a URL or file path
        if any(
            pattern in line
            for pattern in ("http://", "https://", "file://", "../", "./", "\\", "/")
        ):
            # Check if the word is part of a path or URL
            for sep in ("/", "\\", "."):
                if (word_pos_in_line > 0 and line[word_pos_in_line - 1] == sep) or (
                    word_pos_in_line + len(word) < len(line)
                    and line[word_pos_in_line + len(word)] == sep
                ):
                    return True

        return False

    def check_file(self, filepath: Path) -> bool:
        """Check a single file for message references.

        Args:
            filepath: Path to the file to check

        Returns:
            True if the file has no issues or all issues were fixed
        """
        if filepath.suffix not in self.VALID_EXTENSIONS:
            return True

        try:
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"Error reading {filepath}: {e}")
            return False

        original_content = content
        issues_in_file = []

        # Find all potential message references
        for match in self.DASH_WORD_PATTERN.finditer(original_content):
            if not self._should_skip_match(original_content, match, filepath):
                word = match.group(1)
                issues_in_file.append((match.start(), match.end(), word))

        if not issues_in_file:
            if self.verbose:
                print(f"✓ {filepath}: No issues found")
            return True

        # Report or fix issues
        self.issues_found += len(issues_in_file)

        if self.fix:
            # Build a list of replacements
            replacements = []
            for start, end, word in issues_in_file:
                ref = f":ref:`{word}`"
                replacements.append((start, end, ref))

            # Apply replacements from end to start to maintain string positions
            replacements.sort(key=lambda x: x[0], reverse=True)
            modified_content = content
            for start, end, replacement in replacements:
                modified_content = (
                    modified_content[:start] + replacement + modified_content[end:]
                )

            # Only write if content actually changed
            if modified_content != original_content:
                try:
                    return self.fix_the_file(
                        filepath, issues_in_file, modified_content, original_content
                    )
                except OSError as e:
                    print(f"Error writing {filepath}: {e}")
                    return False
            else:
                print(f"⚠ {filepath}: No changes made (content unchanged)")
                return True
        else:
            # Report issues
            print(f"✗ {filepath}: Found {len(issues_in_file)} issue(s):")

            # Show context for each issue
            lines = original_content.split("\n")
            for start, _, word in issues_in_file:
                line_num = original_content[:start].count("\n") + 1
                col = start - original_content.rfind("\n", 0, start) - 1

                # Get the line and highlight the issue
                if line_num <= len(lines):
                    line = lines[line_num - 1]
                    print(f"  Line {line_num}:{col}: '{word}' should be :ref:`{word}`")
                    if self.verbose:
                        print(f"    {line.strip()}")

            return False

    def fix_the_file(
        self,
        filepath: str | Path,
        issues_in_file: list[tuple[int, int, str]],
        modified_content: str,
        original_content: str,
    ) -> bool:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(modified_content)
        self.files_fixed += 1
        print(f"✓ {filepath}: Fixed {len(issues_in_file)} reference(s)")
        # Show what was changed if verbose
        if self.verbose:
            for start, _, word in issues_in_file:
                line_num = original_content[:start].count("\n") + 1
                print(f"    Line {line_num}: '{word}' → :ref:`{word}`")
        return True

    def check_files(self, filenames: list[str]) -> bool:
        """Check multiple files.

        Args:
            filenames: List of file paths to check

        Returns:
            True if all files have no issues or all issues were fixed
        """
        all_good = True

        for filename in filenames:
            filepath = Path(filename)
            if not filepath.exists():
                print(f"Warning: {filepath} does not exist")
                continue

            if not self.check_file(filepath):
                all_good = False

        # Print summary
        if self.issues_found > 0:
            if self.fix:
                print(
                    f"\nSummary: Fixed {self.issues_found} reference(s) in {self.files_fixed} file(s)"
                )
            else:
                print(f"\nSummary: Found {self.issues_found} issue(s)")
                print("Run with --fix to automatically fix these issues")
        elif self.verbose:
            print("\nNo issues found!")

        return all_good


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Check and fix pylint message references in documentation files"
    )
    parser.add_argument("filenames", nargs="*", help="Files to check")
    parser.add_argument("--fix", action="store_true", help="Automatically fix issues")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args(argv)

    if not args.filenames:
        print("No files specified")
        return 1

    checker = MessageReferenceChecker(verbose=args.verbose, fix=args.fix)
    success = checker.check_files(args.filenames)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
