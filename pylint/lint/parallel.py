# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import functools
import warnings
from collections import defaultdict
from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, Any

import dill

from pylint import reporters
from pylint.config.find_default_config_files import find_default_config_files
from pylint.lint.utils import _patch_sys_path, extract_results_from_linter, insert_results_to_linter, _merge_mapreduce_data
from pylint.message import Message
from pylint.typing import FileItem
from pylint.utils import LinterStats, merge_stats

try:
    import multiprocessing
except ImportError:
    multiprocessing = None  # type: ignore[assignment]

if TYPE_CHECKING:
    from pylint.lint import PyLinter

# PyLinter object used by worker processes when checking files using multiprocessing
# should only be used by the worker processes
_worker_linters: PyLinter | None = None


def _worker_initialize(
    linters: bytes, arguments: None | str | Sequence[str] = None
) -> None:
    """Function called to initialize a worker for a Process within a multiprocessing Pool.

    :param linter: A linter-class (PyLinter) instance pickled with dill
    :param arguments: File or module name(s) to lint and to be added to sys.path
    """
    global _worker_linters  # pylint: disable=global-statement
    _worker_linters = dill.loads(linters)
    assert _worker_linters

    # On the worker process side the messages are just collected and passed back to
    # parent process as _worker_check_file function's return value
    for _worker_linter in _worker_linters.values():
        _worker_linter.set_reporter(reporters.CollectingReporter())
        _worker_linter.open()

    # Patch sys.path so that each argument is importable just like in single job mode
    _patch_sys_path(arguments or ())


def _worker_check_single_file(
    file_item: FileItem,
) -> tuple[
    int,
    # TODO: 3.0: Make this only str after deprecation has been removed # pylint: disable=fixme
    str | None,
    str,
    str | None,
    list[Message],
    LinterStats,
    int,
    defaultdict[str, list[Any]],
]:
    rcfiles = file_item[0]
    file_item = file_item[1]

    if not _worker_linters[rcfiles]:
        raise Exception("Worker linter not yet initialised")
    _worker_linters[rcfiles].open()
    _worker_linters[rcfiles].check_single_file_item(file_item)
    (
        linter_current_name,
        _,
        base_name,
        msgs,
        linter_stats,
        linter_msg_status,
        mapreduce_data,
    ) = extract_results_from_linter(_worker_linters[rcfiles])
    return (
        id(multiprocessing.current_process()),
        linter_current_name,
        file_item.filepath,
        base_name,
        msgs,
        linter_stats,
        linter_msg_status,
        mapreduce_data,
    )


def check_parallel(
    linter: PyLinter,
    linters,
    jobs: int,
    files, #[(conf, FileItem)],
    arguments: None | str | Sequence[str] = None,
) -> None:
    """Use the given linter to lint the files with given amount of workers (jobs).

    This splits the work filestream-by-filestream. If you need to do work across
    multiple files, as in the similarity-checker, then implement the map/reduce mixin functionality.
    """
    # The linter is inherited by all the pool's workers, i.e. the linter
    # is identical to the linter object here. This is required so that
    # a custom PyLinter object can be used.
    initializer = functools.partial(_worker_initialize, arguments=arguments)
    with multiprocessing.Pool(
        jobs, initializer=initializer, initargs=[dill.dumps(linters)]
    ) as pool:
        linter.open()
        all_stats = []
        all_mapreduce_data: defaultdict[
            int, list[defaultdict[str, list[Any]]]
        ] = defaultdict(list)

        # Maps each file to be worked on by a single _worker_check_single_file() call,
        # collecting any map/reduce data by checker module so that we can 'reduce' it
        # later.
        for (
            worker_idx,  # used to merge map/reduce data across workers
            module,
            file_path,
            base_name,
            messages,
            stats,
            msg_status,
            mapreduce_data,
        ) in pool.imap_unordered(_worker_check_single_file, files):
            insert_results_to_linter(
                linter, module, file_path, base_name, messages, msg_status
            )
            all_stats.append(stats)
            all_mapreduce_data[worker_idx].append(mapreduce_data)

        pool.close()
        pool.join()

    _merge_mapreduce_data(linter, all_mapreduce_data)
    linter.stats = merge_stats([linter.stats] + all_stats)
