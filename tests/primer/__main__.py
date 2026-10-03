# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from pathlib import Path

from pylint.testutils._primer.primer import Primer

PRIMER_DIRECTORY = Path(__file__).parent.parent / ".pylint_primer_tests/"
PACKAGES_TO_PRIME_PATH = Path(__file__).parent / "packages_to_prime.json"


if __name__ == "__main__":
    primer = Primer(PRIMER_DIRECTORY, PACKAGES_TO_PRIME_PATH)
    primer.run()
