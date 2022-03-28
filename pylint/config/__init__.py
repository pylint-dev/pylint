# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import os
import pathlib
import pickle
import sys
from datetime import datetime

from pylint.config.configuration_mixin import ConfigurationMixIn
from pylint.config.find_default_config_files import (
    find_default_config_files,
    find_pylintrc,
)
from pylint.config.man_help_formatter import _ManHelpFormatter
from pylint.config.option import Option
from pylint.config.option_manager_mixin import OptionsManagerMixIn
from pylint.config.option_parser import OptionParser
from pylint.config.options_provider_mixin import OptionsProviderMixIn, UnsupportedAction
from pylint.constants import DEFAULT_PYLINT_HOME, OLD_DEFAULT_PYLINT_HOME
from pylint.utils import LinterStats

__all__ = [
    "ConfigurationMixIn",
    "find_default_config_files",
    "_ManHelpFormatter",
    "Option",
    "OptionsManagerMixIn",
    "OptionParser",
    "OptionsProviderMixIn",
    "UnsupportedAction",
]

USER_HOME = os.path.expanduser("~")
if "PYLINTHOME" in os.environ:
    PYLINT_HOME = os.environ["PYLINTHOME"]
    if USER_HOME == "~":
        USER_HOME = os.path.dirname(PYLINT_HOME)
elif USER_HOME == "~":
    PYLINT_HOME = OLD_DEFAULT_PYLINT_HOME
else:
    PYLINT_HOME = DEFAULT_PYLINT_HOME
    # The spam prevention is due to pylint being used in parallel by
    # pre-commit, and the message being spammy in this context
    # Also if you work with old version of pylint that recreate the
    # old pylint home, you can get the old message for a long time.
    prefix_spam_prevention = "pylint_warned_about_old_cache_already"
    spam_prevention_file = os.path.join(
        PYLINT_HOME,
        datetime.now().strftime(prefix_spam_prevention + "_%Y-%m-%d.temp"),
    )
    old_home = os.path.join(USER_HOME, OLD_DEFAULT_PYLINT_HOME)
    if os.path.exists(old_home) and not os.path.exists(spam_prevention_file):
        print(
            f"PYLINTHOME is now '{PYLINT_HOME}' but obsolescent '{old_home}' is found; "
            "you can safely remove the latter",
            file=sys.stderr,
        )
        # Remove old spam prevention file
        if os.path.exists(PYLINT_HOME):
            for filename in os.listdir(PYLINT_HOME):
                if prefix_spam_prevention in filename:
                    try:
                        os.remove(os.path.join(PYLINT_HOME, filename))
                    except OSError:
                        pass

        # Create spam prevention file for today
        try:
            pathlib.Path(PYLINT_HOME).mkdir(parents=True, exist_ok=True)
            with open(spam_prevention_file, "w", encoding="utf8") as f:
                f.write("")
        except Exception as exc:  # pylint: disable=broad-except
            print(
                "Can't write the file that was supposed to "
                f"prevent 'pylint.d' deprecation spam in {PYLINT_HOME} because of {exc}."
            )


def _get_pdata_path(base_name, recurs):
    base_name = base_name.replace(os.sep, "_")
    return os.path.join(PYLINT_HOME, f"{base_name}{recurs}.stats")


def load_results(base):
    data_file = _get_pdata_path(base, 1)
    try:
        with open(data_file, "rb") as stream:
            data = pickle.load(stream)
            if not isinstance(data, LinterStats):
                raise TypeError
            return data
    except Exception:  # pylint: disable=broad-except
        return None


def save_results(results, base):
    if not os.path.exists(PYLINT_HOME):
        try:
            os.makedirs(PYLINT_HOME)
        except OSError:
            print(f"Unable to create directory {PYLINT_HOME}", file=sys.stderr)
    data_file = _get_pdata_path(base, 1)
    try:
        with open(data_file, "wb") as stream:
            pickle.dump(results, stream)
    except OSError as ex:
        print(f"Unable to create file {data_file}: {ex}", file=sys.stderr)


PYLINTRC = find_pylintrc()
