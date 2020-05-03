# -*- coding: utf-8 -*-
# Copyright (c) 2006-2010, 2012-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2008 pyves@crater.logilab.fr <pyves@crater.logilab.fr>
# Copyright (c) 2010 Julien Jehannet <julien.jehannet@logilab.fr>
# Copyright (c) 2013 Google, Inc.
# Copyright (c) 2013 John McGehee <jmcgehee@altera.com>
# Copyright (c) 2014-2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2015 John Kirkham <jakirkham@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Erik <erik.eriksson@yahoo.com>
# Copyright (c) 2016 Alexander Todorov <atodorov@otb.bg>
# Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
# Copyright (c) 2017-2019 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2017 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2017 ahirnish <ahirnish@gmail.com>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2018, 2020 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2018 Jim Robertson <jrobertson98atx@gmail.com>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Gary Tyler McLeod <mail@garytyler.com>
# Copyright (c) 2018 Konstantin <Github@pheanex.de>
# Copyright (c) 2018 Nick Drozd <nicholasdrozd@gmail.com>
# Copyright (c) 2019 Janne Rönkkö <jannero@users.noreply.github.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2019 Pierre Sassoulas <pierre.sassoulas@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""utilities for Pylint configuration :

* pylintrc
* pylint.d (PYLINTHOME)
"""
import optparse
import os
import pickle
import sys
from typing import Any, Dict, Tuple

from pylint.config.find_default_config_files import find_default_config_files
from pylint.config.man_help_formatter import _ManHelpFormatter
from pylint.config.option import (
    Option,
    _csv_validator,
    _regexp_csv_validator,
    _regexp_validator,
    _validate,
)
from pylint.config.option_manager_mixin import OptionsManagerMixIn
from pylint.config.option_parser import OptionParser

__all__ = [
    "_csv_validator",
    "_regexp_csv_validator",
    "_regexp_validator",
    "OptionsManagerMixIn",
]

USER_HOME = os.path.expanduser("~")
if "PYLINTHOME" in os.environ:
    PYLINT_HOME = os.environ["PYLINTHOME"]
    if USER_HOME == "~":
        USER_HOME = os.path.dirname(PYLINT_HOME)
elif USER_HOME == "~":
    PYLINT_HOME = ".pylint.d"
else:
    PYLINT_HOME = os.path.join(USER_HOME, ".pylint.d")


def _get_pdata_path(base_name, recurs):
    base_name = base_name.replace(os.sep, "_")
    return os.path.join(PYLINT_HOME, "%s%s%s" % (base_name, recurs, ".stats"))


def load_results(base):
    data_file = _get_pdata_path(base, 1)
    try:
        with open(data_file, "rb") as stream:
            return pickle.load(stream)
    except Exception:  # pylint: disable=broad-except
        return {}


def save_results(results, base):
    if not os.path.exists(PYLINT_HOME):
        try:
            os.mkdir(PYLINT_HOME)
        except OSError:
            print("Unable to create directory %s" % PYLINT_HOME, file=sys.stderr)
    data_file = _get_pdata_path(base, 1)
    try:
        with open(data_file, "wb") as stream:
            pickle.dump(results, stream)
    except OSError as ex:
        print("Unable to create file %s: %s" % (data_file, ex), file=sys.stderr)


def find_pylintrc():
    """search the pylint rc file and return its path if it find it, else None
    """
    for config_file in find_default_config_files():
        if config_file.endswith("pylintrc"):
            return config_file

    return None


PYLINTRC = find_pylintrc()

ENV_HELP = (
    """
The following environment variables are used:
    * PYLINTHOME
    Path to the directory where persistent data for the run will be stored. If
not found, it defaults to ~/.pylint.d/ or .pylint.d (in the current working
directory).
    * PYLINTRC
    Path to the configuration file. See the documentation for the method used
to search for configuration file.
"""
    % globals()  # type: ignore
)


class UnsupportedAction(Exception):
    """raised by set_option when it doesn't know what to do for an action"""

class OptionsProviderMixIn:
    """Mixin to provide options to an OptionsManager"""

    # those attributes should be overridden
    priority = -1
    name = "default"
    options = ()  # type: Tuple[Tuple[str, Dict[str, Any]], ...]
    level = 0

    def __init__(self):
        self.config = optparse.Values()
        self.load_defaults()

    def load_defaults(self):
        """initialize the provider using default values"""
        for opt, optdict in self.options:
            action = optdict.get("action")
            if action != "callback":
                # callback action have no default
                if optdict is None:
                    optdict = self.get_option_def(opt)
                default = optdict.get("default")
                self.set_option(opt, default, action, optdict)

    def option_attrname(self, opt, optdict=None):
        """get the config attribute corresponding to opt"""
        if optdict is None:
            optdict = self.get_option_def(opt)
        return optdict.get("dest", opt.replace("-", "_"))

    def option_value(self, opt):
        """get the current value for the given option"""
        return getattr(self.config, self.option_attrname(opt), None)

    def set_option(self, optname, value, action=None, optdict=None):
        """method called to set an option (registered in the options list)"""
        if optdict is None:
            optdict = self.get_option_def(optname)
        if value is not None:
            value = _validate(value, optdict, optname)
        if action is None:
            action = optdict.get("action", "store")
        if action == "store":
            setattr(self.config, self.option_attrname(optname, optdict), value)
        elif action in ("store_true", "count"):
            setattr(self.config, self.option_attrname(optname, optdict), 0)
        elif action == "store_false":
            setattr(self.config, self.option_attrname(optname, optdict), 1)
        elif action == "append":
            optname = self.option_attrname(optname, optdict)
            _list = getattr(self.config, optname, None)
            if _list is None:
                if isinstance(value, (list, tuple)):
                    _list = value
                elif value is not None:
                    _list = []
                    _list.append(value)
                setattr(self.config, optname, _list)
            elif isinstance(_list, tuple):
                setattr(self.config, optname, _list + (value,))
            else:
                _list.append(value)
        elif action == "callback":
            optdict["callback"](None, optname, value, None)
        else:
            raise UnsupportedAction(action)

    def get_option_def(self, opt):
        """return the dictionary defining an option given its name"""
        assert self.options
        for option in self.options:
            if option[0] == opt:
                return option[1]
        raise optparse.OptionError(
            "no such option %s in section %r" % (opt, self.name), opt
        )

    def options_by_section(self):
        """return an iterator on options grouped by section

        (section, [list of (optname, optdict, optvalue)])
        """
        sections = {}
        for optname, optdict in self.options:
            sections.setdefault(optdict.get("group"), []).append(
                (optname, optdict, self.option_value(optname))
            )
        if None in sections:
            yield None, sections.pop(None)
        for section, options in sorted(sections.items()):
            yield section.upper(), options

    def options_and_values(self, options=None):
        if options is None:
            options = self.options
        for optname, optdict in options:
            yield (optname, optdict, self.option_value(optname))


class ConfigurationMixIn(OptionsManagerMixIn, OptionsProviderMixIn):
    """basic mixin for simple configurations which don't need the
    manager / providers model
    """

    def __init__(self, *args, **kwargs):
        if not args:
            kwargs.setdefault("usage", "")
        OptionsManagerMixIn.__init__(self, *args, **kwargs)
        OptionsProviderMixIn.__init__(self)
        if not getattr(self, "option_groups", None):
            self.option_groups = []
            for _, optdict in self.options:
                try:
                    gdef = (optdict["group"].upper(), "")
                except KeyError:
                    continue
                if gdef not in self.option_groups:
                    self.option_groups.append(gdef)
        self.register_options_provider(self, own_group=False)
