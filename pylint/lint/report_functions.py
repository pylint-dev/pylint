# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import collections
from typing import DefaultDict, Dict, List, Tuple, Union

from pylint import checkers, exceptions
from pylint.reporters.ureports import nodes as report_nodes
from pylint.typing import CheckerStats


def report_total_messages_stats(
    sect,
    stats: CheckerStats,
    previous_stats: CheckerStats,
):
    """make total errors / warnings report"""
    lines = ["type", "number", "previous", "difference"]
    lines += checkers.table_lines_from_stats(
        stats, previous_stats, ("convention", "refactor", "warning", "error")
    )
    sect.append(report_nodes.Table(children=lines, cols=4, rheaders=1))


def report_messages_stats(
    sect,
    stats: CheckerStats,
    _: CheckerStats,
):
    """make messages type report"""
    if not stats["by_msg"]:
        # don't print this report when we didn't detected any errors
        raise exceptions.EmptyReportError()
    by_msg_stats: Dict[str, int] = stats["by_msg"]  # type: ignore
    in_order: List[Tuple[int, str]] = sorted(
        (value, msg_id)
        for msg_id, value in by_msg_stats.items()
        if not msg_id.startswith("I")
    )
    in_order.reverse()
    lines = ["message id", "occurrences"]
    for value, msg_id in in_order:
        lines += [msg_id, str(value)]
    sect.append(report_nodes.Table(children=lines, cols=2, rheaders=1))


def report_messages_by_module_stats(
    sect,
    stats: CheckerStats,
    _: CheckerStats,
):
    """make errors / warnings by modules report"""
    module_stats: Dict[str, Dict[str, int]] = stats["by_module"]  # type: ignore
    if len(module_stats) == 1:
        # don't print this report when we are analysing a single module
        raise exceptions.EmptyReportError()
    by_mod: DefaultDict[str, Dict[str, Union[int, float]]] = collections.defaultdict(
        dict
    )
    for m_type in ("fatal", "error", "warning", "refactor", "convention"):
        total: int = stats[m_type]  # type: ignore
        for module in module_stats.keys():
            mod_total = module_stats[module][m_type]
            percent = 0 if total == 0 else float((mod_total) * 100) / total
            by_mod[module][m_type] = percent
    sorted_result = []
    for module, mod_info in by_mod.items():
        sorted_result.append(
            (
                mod_info["error"],
                mod_info["warning"],
                mod_info["refactor"],
                mod_info["convention"],
                module,
            )
        )
    sorted_result.sort()
    sorted_result.reverse()
    lines = ["module", "error", "warning", "refactor", "convention"]
    for line in sorted_result:
        # Don't report clean modules.
        if all(entry == 0 for entry in line[:-1]):
            continue
        lines.append(line[-1])
        for val in line[:-1]:
            lines.append(f"{val:.2f}")
    if len(lines) == 5:
        raise exceptions.EmptyReportError()
    sect.append(report_nodes.Table(children=lines, cols=5, rheaders=1))
