# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Sphinx role for referencing pylint messages."""

from __future__ import annotations

from typing import TYPE_CHECKING

from docutils import nodes
from sphinx.util.docutils import SphinxRole

if TYPE_CHECKING:
    from sphinx.application import Sphinx

# Cache for message lookups to avoid repeated initialization
_message_cache: dict[str, str] | None = None


def _get_message_category_map() -> dict[str, str]:
    """Get a mapping of message names to their categories.

    Returns a dict mapping message symbol (e.g., 'used-before-assignment')
    to category (e.g., 'error').
    """
    global _message_cache

    if _message_cache is not None:
        return _message_cache

    from pylint.checkers import initialize as initialize_checkers
    from pylint.constants import MSG_TYPES
    from pylint.extensions import initialize as initialize_extensions
    from pylint.lint import PyLinter

    # Create mapping of message type codes to category names
    msg_types_doc = {
        k: v if v != "info" else "information" for k, v in MSG_TYPES.items()
    }

    # Initialize linter and register all checkers
    linter = PyLinter()
    initialize_checkers(linter)
    initialize_extensions(linter)

    # Build the cache
    _message_cache = {}
    for checker in linter.get_checkers():
        for message in checker.messages:
            category = msg_types_doc[message.msgid[0]]
            _message_cache[message.symbol] = category

    return _message_cache


class PylintMessageRole(SphinxRole):
    """Custom Sphinx role for referencing pylint messages.

    Usage:
        :pylint:`used-before-assignment`

    This will create a link to the message documentation page.
    """

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        """Execute the role."""
        message_name = self.text.strip()

        # Get the category for this message
        category_map = _get_message_category_map()

        if message_name not in category_map:
            # Message not found - create a warning but still create a node
            msg = self.state_machine.reporter.warning(
                f"Unknown pylint message: {message_name}",
                line=self.lineno,
            )
            # Create a simple text node instead of a link
            node = nodes.Text(message_name, message_name)
            return [node], [msg]

        category = category_map[message_name]

        # Create the reference node
        # The target URL is relative to the current document
        refuri = f"../user_guide/messages/{category}/{message_name}.html"

        node = nodes.reference(
            self.rawtext,
            message_name,
            refuri=refuri,
            **self.options,
        )

        return [node], []


def setup(app: Sphinx) -> dict[str, bool]:
    """Set up the Sphinx extension."""
    app.add_role("pylint", PylintMessageRole())

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
