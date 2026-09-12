# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pylint.testutils._primer import PackageToLint


def get_argument_parser(prog: str, *, with_batches: bool) -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(prog=prog)
    subparsers = argument_parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument(
        "--clone", help="Clone all packages.", action="store_true", default=False
    )
    prepare_parser.add_argument(
        "--check",
        help="Check consistencies and commits of all packages.",
        action="store_true",
        default=False,
    )
    prepare_parser.add_argument(
        "--make-commit-string",
        help="Get latest commit string.",
        action="store_true",
        default=False,
    )
    prepare_parser.add_argument(
        "--read-commit-string",
        help="Print latest commit string.",
        action="store_true",
        default=False,
    )

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument(
        "--type", choices=["main", "pr"], required=True, help="Type of primer run."
    )
    if with_batches:
        run_parser.add_argument(
            "--batches",
            required=False,
            type=int,
            help="Number of batches",
        )
        run_parser.add_argument(
            "--batchIdx",
            required=False,
            type=int,
            help="Portion of primer packages to run.",
        )

    compare_parser = subparsers.add_parser("compare")
    compare_parser.add_argument(
        "--base-file",
        required=True,
        help="Location of output file of the base run.",
    )
    compare_parser.add_argument(
        "--new-file",
        required=True,
        help="Location of output file of the new run.",
    )
    compare_parser.add_argument(
        "--commit",
        required=True,
        help="Commit hash of the PR commit being checked.",
    )
    if with_batches:
        compare_parser.add_argument(
            "--batches",
            required=False,
            type=int,
            help=(
                "Number of batches (filepaths with the placeholder BATCHIDX will be "
                "numbered)"
            ),
        )

    return argument_parser


def minimum_python_supported(package_data: dict[str, object]) -> bool:
    min_python_str = package_data.get("minimum_python", None)
    if not min_python_str:
        return True
    min_python_tuple = tuple(int(n) for n in str(min_python_str).split("."))
    return min_python_tuple <= sys.version_info[:2]


def get_packages_to_prime_from_json(json_path: Path) -> dict[str, PackageToLint]:
    with open(json_path, encoding="utf-8") as stream:
        return {
            name: PackageToLint(**package_data)
            for name, package_data in json.load(stream).items()
            if minimum_python_supported(package_data)
        }
