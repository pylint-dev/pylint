# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path
from typing import Any

from pylint.constants import PYLINT_HOME
from pylint.utils import LinterStats

PYLINT_HOME_AS_PATH = Path(PYLINT_HOME)


def _get_pdata_path(
    base_name: Path, recurs: int, pylint_home: Path = PYLINT_HOME_AS_PATH
) -> Path:
    # We strip all characters that can't be used in a filename. Also strip '/' and
    # '\\' because we want to create a single file, not sub-directories.
    underscored_name = "_".join(
        str(p.replace(":", "_").replace("/", "_").replace("\\", "_"))
        for p in base_name.parts
    )
    return pylint_home / f"{underscored_name}_{recurs}.stats"


def _stats_to_dict(stats: LinterStats) -> dict[str, Any]:
    """Turn ``stats`` into a JSON-serializable dict.

    Every field is JSON-native except the two ``set`` fields, which are stored as
    lists and rebuilt in :func:`_stats_from_dict`.
    """
    data = dict(stats.__dict__)
    data["modules_names"] = sorted(stats.modules_names)
    data["dependencies"] = {
        module: sorted(deps) for module, deps in stats.dependencies.items()
    }
    return data


def _stats_from_dict(data: dict[str, Any]) -> LinterStats:
    """Inverse of :func:`_stats_to_dict`."""
    stats = LinterStats()
    stats.__dict__.update(data)
    stats.modules_names = set(data.get("modules_names", []))
    stats.dependencies = {
        module: set(deps) for module, deps in data.get("dependencies", {}).items()
    }
    return stats


def load_results(
    base: str | Path, pylint_home: str | Path = PYLINT_HOME
) -> LinterStats | None:
    base = Path(base)
    pylint_home = Path(pylint_home)
    data_file = _get_pdata_path(base, 1, pylint_home)

    if not data_file.exists():
        return None

    try:
        with open(data_file, encoding="utf-8") as stream:
            data = json.load(stream)
        stats = _stats_from_dict(data) if isinstance(data, dict) else data
        if not isinstance(stats, LinterStats):
            warnings.warn(
                "You're using an old pylint cache with invalid data following "
                f"an upgrade, please delete '{data_file}'.",
                UserWarning,
                stacklevel=2,
            )
            raise TypeError
        return stats
    except Exception:  # pylint: disable=broad-except
        # There's an issue with the cache but we just continue as if it isn't
        # there. pylint never loads a cache file with pickle.
        return None


def save_results(
    results: LinterStats, base: str | Path, pylint_home: str | Path = PYLINT_HOME
) -> None:
    base = Path(base)
    pylint_home = Path(pylint_home)
    try:
        pylint_home.mkdir(parents=True, exist_ok=True)
    except OSError:  # pragma: no cover
        print(f"Unable to create directory {pylint_home}", file=sys.stderr)
    data_file = _get_pdata_path(base, 1, pylint_home)
    try:
        with open(data_file, "w", encoding="utf-8") as stream:
            json.dump(_stats_to_dict(results), stream)
    except OSError as ex:  # pragma: no cover
        print(f"Unable to create file {data_file}: {ex}", file=sys.stderr)
