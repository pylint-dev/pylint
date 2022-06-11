#!/usr/bin/env python

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Custom extension to automatically generate changelog sections
from GitHub issues.
"""
from __future__ import annotations

import re
from collections.abc import Iterable

from docutils import frontend, nodes
from docutils.parsers.rst import directives
from docutils.utils import new_document
from github3 import login  # type: ignore[import]
from github3.search.issue import IssueSearchResult  # type: ignore[import]
from myst_parser.docutils_ import Parser  # type: ignore[import]
from sphinx.application import Sphinx
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

logger = logging.getLogger(__name__)


class ChangelogDirective(SphinxDirective):
    option_spec = {
        "query": directives.unchanged_required,
        "caption": directives.unchanged,
        "hide_if_empty": directives.flag,
    }
    has_content = True
    parser = Parser()
    changelog_pattern = re.compile(
        r"<!-- changelog start -->\n(?P<entry>(.*\n)*)<!-- changelog end -->",
        flags=re.MULTILINE,
    )

    def run(self):
        if not self.config.pylint_changelog_token:
            logger.info(
                "No Github token provided. Changelog generation will be skipped."
            )
            return []
        result = []
        caption = self.options.get("caption")
        if caption:
            result.append(nodes.title(text=caption))
        list_node = nodes.bullet_list(
            "",
            *(
                self._build_changelog_entry(issue)
                for issue in self._get_relevant_issues()
            ),
        )
        result.append(list_node)
        logger.info("Found %d issues for this query.", len(list_node))
        if not list_node and self.options.get("hide_if_empty", False):
            logger.info("Flag 'hide_if_empty' is set, hiding this section.")
            return []
        return result

    def _get_relevant_issues(self) -> Iterable[IssueSearchResult]:
        full_query = self._build_query()
        gh = login(token=self.config.pylint_changelog_token)
        logger.info("Searching for issues/pull requests matching query %s", full_query)
        return gh.search_issues(query=full_query)

    def _build_query(self) -> str:
        user = self.config.pylint_changelog_user
        project = self.config.pylint_changelog_project
        query = self.options.get("query")
        full_query = f"repo:{user}/{project} {query}"
        for excluded_label in self.config.pylint_changelog_exclude_labels:
            full_query += f' -label:"{excluded_label}"'
        return full_query

    def _build_changelog_entry(self, issue: IssueSearchResult) -> nodes.list_item:
        match = self.changelog_pattern.search(issue.body)
        if match:
            text = match.group("entry").strip()
        else:
            logger.warning(
                "PR #%d is missing the changelog section. "
                "Using the PR title as substitute.",
                issue.number,
            )
            text = issue.title
        text += f"\n\nPR: [#{issue.number}](https://github.com/PyCQA/pylint/pull/{issue.number})"
        return nodes.list_item("", *self._parse_markdown(text).children)

    def _parse_markdown(self, text: str) -> nodes.document:
        parser = Parser()
        components = (Parser,)
        settings = frontend.OptionParser(components=components).get_default_values()
        document = new_document("", settings=settings)
        parser.parse(text, document)
        return document


def setup(app: Sphinx) -> dict[str, str | bool]:
    app.add_config_value("pylint_changelog_user", None, "html")
    app.add_config_value("pylint_changelog_project", None, "html")
    app.add_config_value("pylint_changelog_token", None, "html")
    app.add_config_value("pylint_changelog_exclude_labels", [], "html")
    app.add_directive("changelog", ChangelogDirective)
    return {"version": "0.1", "parallel_read_safe": True}
