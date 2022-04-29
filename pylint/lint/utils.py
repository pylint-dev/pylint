# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import contextlib
import sys
import traceback
from collections import defaultdict
from collections.abc import Iterator, Sequence
from datetime import datetime
from pathlib import Path

from pylint import reporters
from pylint.utils import merge_stats
from pylint.config import PYLINT_HOME
from pylint.lint.expand_modules import get_python_path


def prepare_crash_report(ex: Exception, filepath: str, crash_file_path: str) -> Path:
    issue_template_path = (
        Path(PYLINT_HOME) / datetime.now().strftime(str(crash_file_path))
    ).resolve()
    with open(filepath, encoding="utf8") as f:
        file_content = f.read()
    template = ""
    if not issue_template_path.exists():
        template = """\
First, please verify that the bug is not already filled:
https://github.com/PyCQA/pylint/issues/

Then create a new crash issue:
https://github.com/PyCQA/pylint/issues/new?assignees=&labels=crash%2Cneeds+triage&template=BUG-REPORT.yml

"""
    template += f"""\

Issue title:
Crash ``{ex}`` (if possible, be more specific about what made pylint crash)
Content:
When parsing the following file:

<!--
 If sharing the code is not an option, please state so,
 but providing only the stacktrace would still be helpful.
 -->

```python
{file_content}
```

pylint crashed with a ``{ex.__class__.__name__}`` and with the following stacktrace:
```
"""
    template += traceback.format_exc()
    template += "```\n"
    try:
        with open(issue_template_path, "a", encoding="utf8") as f:
            f.write(template)
    except Exception as exc:  # pylint: disable=broad-except
        print(
            f"Can't write the issue template for the crash in {issue_template_path} "
            f"because of: '{exc}'\nHere's the content anyway:\n{template}."
        )
    return issue_template_path


def get_fatal_error_message(filepath: str, issue_template_path: Path) -> str:
    return (
        f"Fatal error while checking '{filepath}'. "
        f"Please open an issue in our bug tracker so we address this. "
        f"There is a pre-filled template that you can use in '{issue_template_path}'."
    )


def _patch_sys_path(args: Sequence[str]) -> list[str]:
    original = list(sys.path)
    changes = []
    seen = set()
    for arg in args:
        path = get_python_path(arg)
        if path not in seen:
            changes.append(path)
            seen.add(path)

    sys.path[:] = changes + sys.path
    return original


@contextlib.contextmanager
def fix_import_path(args: Sequence[str]) -> Iterator[None]:
    """Prepare 'sys.path' for running the linter checks.

    Within this context, each of the given arguments is importable.
    Paths are added to 'sys.path' in corresponding order to the arguments.
    We avoid adding duplicate directories to sys.path.
    `sys.path` is reset to its original value upon exiting this context.
    """
    original = _patch_sys_path(args)
    try:
        yield
    finally:
        sys.path[:] = original


def insert_results_to_linter(
    linter, module, file_path, base_name, messages, msg_status
):
    linter.file_state.base_name = base_name
    linter.set_current_module(module, file_path)
    for msg in messages:
        linter.reporter.handle_message(msg)
    linter.msg_status |= msg_status


def extract_results_from_linter(linter):
    mapreduce_data = defaultdict(list)
    for checker in linter.get_checkers():
        data = checker.get_map_data()
        if data is not None:
            mapreduce_data[checker.name].append(data)
    msgs = linter.reporter.messages
    assert isinstance(linter.reporter, reporters.CollectingReporter)
    linter.reporter.reset()
    if linter.current_name is None:
        warnings.warn(
            (
                "In pylint 3.0 the current_name attribute of the linter object should be a string. "
                "If unknown it should be initialized as an empty string."
            ),
            DeprecationWarning,
        )
    return (
        linter.current_name,
        "bla",  # FIXME before: # file_item.filepath,
        linter.file_state.base_name,
        msgs,
        linter.stats,
        linter.msg_status,
        mapreduce_data,
    )


def _merge_mapreduce_data(
    linter: PyLinter,
    all_mapreduce_data: defaultdict[int, list[defaultdict[str, list[Any]]]],
) -> None:
    """Merges map/reduce data across workers, invoking relevant APIs on checkers."""
    # First collate the data and prepare it, so we can send it to the checkers for
    # validation. The intent here is to collect all the mapreduce data for all checker-
    # runs across processes - that will then be passed to a static method on the
    # checkers to be reduced and further processed.
    collated_map_reduce_data: defaultdict[str, list[Any]] = defaultdict(list)
    for linter_data in all_mapreduce_data.values():
        for run_data in linter_data:
            for checker_name, data in run_data.items():
                collated_map_reduce_data[checker_name].extend(data)

    # Send the data to checkers that support/require consolidated data
    original_checkers = linter.get_checkers()
    for checker in original_checkers:
        if checker.name in collated_map_reduce_data:
            # Assume that if the check has returned map/reduce data that it has the
            # reducer function
            checker.reduce_map_data(linter, collated_map_reduce_data[checker.name])


def merge_linters(dst_linter, *src_linters):
    all_stats = []
    all_mapreduce_data: defaultdict[
        Any, list[defaultdict[str, list[Any]]]
    ] = defaultdict(list)
    for src_linter in src_linters:
        (
            module,
            file_path,
            base_name,
            messages,
            stats,
            msg_status,
            mapreduce_data,
        ) = extract_results_from_linter(src_linter)
        all_stats.append(stats)
        insert_results_to_linter(
            dst_linter, module, file_path, base_name, messages, msg_status
        )
        all_mapreduce_data[src_linter].append(mapreduce_data)

    _merge_mapreduce_data(dst_linter, all_mapreduce_data)
    dst_linter.stats = merge_stats([dst_linter.stats] + all_stats)
