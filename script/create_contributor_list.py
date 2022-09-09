# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from pathlib import Path

from contributors_txt import create_contributors_txt

BASE_DIRECTORY = Path(__file__).parent.parent
ALIASES_FILE = BASE_DIRECTORY / "script/.contributors_aliases.json"
DEFAULT_CONTRIBUTOR_PATH = BASE_DIRECTORY / "CONTRIBUTORS.txt"


def main() -> None:
    create_contributors_txt(
        aliases_file=ALIASES_FILE, output=DEFAULT_CONTRIBUTOR_PATH, verbose=True
    )


if __name__ == "__main__":
    main()
