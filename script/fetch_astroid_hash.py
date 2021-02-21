#!/bin/python
"""Small script to fetch last commit hash for tracked astroid branch."""
import json
import subprocess
import sys
from typing import List

REQUIREMENTS_FILE = "requirements_test_pypy.txt"
GITHUB_API_URI = "https://api.github.com/repos/PyCQA/astroid/branches/"


class ScriptError(Exception):
    pass


def read_branch_from_file(file: str) -> str:
    with open(file) as fp:
        data: List[str] = fp.read().split("\n")
    astroid = [line.strip() for line in data if line.strip().startswith("astroid")]
    if len(astroid) == 0:
        raise ScriptError(f"No astroid dependency found in: {file}")
    if len(astroid) > 1:
        raise ScriptError(f"Multiple astroid dependencies found in: {file}")

    return astroid[0].split("@")[2]


def fetch_hash(branch: str) -> str:
    uri = f"{GITHUB_API_URI}{branch}"
    p = subprocess.run(["curl", "-s", uri], stdout=subprocess.PIPE, check=True)
    if p.stdout is False:
        raise ScriptError(f"Could not fetch API result from: {uri}")
    json_dict = json.loads(p.stdout.decode("utf-8"))
    try:
        return json_dict["commit"]["sha"]
    except KeyError as ex:
        raise ScriptError("Could not read hash") from ex


def main():
    branch = read_branch_from_file(REQUIREMENTS_FILE)
    commit_hash = fetch_hash(branch)
    sys.stdout.write(commit_hash)


if __name__ == "__main__":
    main()
