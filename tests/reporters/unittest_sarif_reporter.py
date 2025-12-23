# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

import io
import json
import os
from pathlib import Path

import pytest
import requests
from astroid import nodes

from pylint import __version__, checkers
from pylint.lint import PyLinter
from pylint.reporters import SARIFReporter

SCHEMA_VERSION = "2.1.0"
CACHE_KEY = f"SCHEMA_{SCHEMA_VERSION}"
SCHEMA_URL = "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json"


def test_simple_sarif() -> None:
    output = io.StringIO()
    reporter = SARIFReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.open()
    linter.set_current_module(
        "0123",
        os.fspath(Path("foo", "bar", "0123")),
    )
    linter.add_message(
        "line-too-long", line=1, args=(1, 2), end_lineno=1, end_col_offset=4
    )
    reporter.display_messages(None)
    assert json.loads(output.getvalue()) == {
        "version": SCHEMA_VERSION,
        "$schema": SCHEMA_URL,
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "pylint",
                        "fullName": f"pylint {__version__}",
                        "version": __version__,
                        "informationUri": "https://pylint.readthedocs.io/",
                        "rules": [
                            {
                                "id": "C0301",
                                "deprecatedIds": [],
                                "name": "line-too-long",
                                "deprecatedNames": [],
                                "shortDescription": {
                                    "text": "Used when a line is longer than a given number of characters"
                                },
                                "fullDescription": {
                                    "text": "Used when a line is longer than a given number of characters."
                                },
                                "help": {
                                    "text": ":line-too-long (C0301): *Line too long (%s/%s)*\n  "
                                    "Used when a line is longer than a given number of characters."
                                },
                                "helpUri": "https://pylint.readthedocs.io/en/stable/user_guide/messages/convention/line-too-long.html",
                            }
                        ],
                    },
                },
                "results": [
                    {
                        "ruleId": "C0301",
                        "message": {"text": "Line too long (1/2)"},
                        "level": "note",
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {
                                        "uri": "foo/bar/0123",
                                    },
                                    "region": {
                                        "startLine": 1,
                                        "startColumn": 1,
                                        "endLine": 1,
                                        "endColumn": 5,
                                    },
                                },
                            }
                        ],
                        "partialFingerprints": {"nodePath/v1": ""},
                    }
                ],
            }
        ],
    }


def test_sarif_node() -> None:
    output = io.StringIO()
    reporter = SARIFReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.open()
    linter.set_current_module("0123")
    mod = nodes.Module("bar", "baz")
    fn = nodes.FunctionDef(
        "foo", lineno=1, col_offset=1, parent=mod, end_lineno=42, end_col_offset=86
    )
    linter.add_message(
        "multiple-statements",
        node=nodes.Import(
            names=[("io", None), ("echo", None)],
            parent=fn,
            lineno=1,
            end_lineno=1,
            end_col_offset=4,
        ),
    )
    reporter.display_messages(None)
    result = json.loads(output.getvalue())["runs"][0]["results"][0]
    assert result["ruleId"] == "C0321"
    assert result["locations"][0]["logicalLocations"] == [
        {
            "name": "foo",
            "fullyQualifiedName": "bar.foo",
        }
    ]


def test_sarif_schema(pytestconfig: pytest.Config) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = pytestconfig.cache.get(CACHE_KEY, None)
    if not schema:
        try:
            res = requests.get(SCHEMA_URL, timeout=5)
        except requests.exceptions.RequestException as e:
            raise pytest.skip(
                f"Unable to retrieve schema v{SCHEMA_VERSION}: {e}"
            ) from e

        if res.status_code != 200:
            raise pytest.skip(
                f"Unable to retrieve schema v{SCHEMA_VERSION}: {res.reason}"
            )
        schema = res.text
        pytestconfig.cache.set(CACHE_KEY, schema)

    output = io.StringIO()
    reporter = SARIFReporter(output)
    linter = PyLinter(reporter=reporter)
    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.open()
    linter.set_current_module("0123")
    linter.add_message(
        "line-too-long", line=1, args=(1, 2), end_lineno=1, end_col_offset=4
    )
    reporter.display_messages(None)

    output.seek(0)
    jsonschema.validate(json.load(output), json.loads(schema))
