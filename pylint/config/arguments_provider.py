# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Arguments provider class used to expose options."""


import optparse  # pylint: disable=deprecated-module
from typing import Dict

from pylint.config.arguments_manager import _ArgumentsManager
from pylint.config.callback_actions import _CallbackAction
from pylint.config.option import _validate
from pylint.typing import Options


class UnsupportedAction(Exception):
    """Raised by set_option when it doesn't know what to do for an action."""


class _ArgumentsProvider:
    """Base class for classes that provide arguments."""

    name: str
    """Name of the provider."""

    options: Options = ()
    """Options provided by this provider."""

    option_groups_descs: Dict[str, str] = {}
    """Option groups of this provider and their descriptions."""

    def __init__(self, arguments_manager: _ArgumentsManager) -> None:
        self._arguments_manager = arguments_manager
        """The manager that will parse and register any options provided."""

        self._arguments_manager._register_options_provider(self)

        # pylint: disable=fixme
        # TODO: Optparse: Added to keep API parity with OptionsProvider
        # They should be removed/deprecated when refactoring the copied methods
        self.config = optparse.Values()
        self.load_defaults()
        self.level = 0

    # pylint: disable-next=fixme
    # TODO: Optparse: All methods below this line are copied to keep API-parity with
    # OptionsProviderMixIn. They should either be deprecated or moved above this line
    # to keep them in _ArgumentsProvider

    def load_defaults(self):
        """Initialize the provider using default values."""
        for opt, optdict in self.options:
            action = optdict.get("action")
            if action != "callback":
                # callback action have no default
                if optdict is None:
                    optdict = self.get_option_def(opt)
                default = optdict.get("default")
                self.set_option(opt, default, action, optdict)

    def option_attrname(self, opt, optdict=None):
        """Get the config attribute corresponding to opt."""
        if optdict is None:
            optdict = self.get_option_def(opt)
        return optdict.get("dest", opt.replace("-", "_"))

    def option_value(self, opt):
        """Get the current value for the given option."""
        return getattr(self.config, self.option_attrname(opt), None)

    def set_option(self, optname, value, action=None, optdict=None):
        """Method called to set an option (registered in the options list)."""
        if optdict is None:
            optdict = self.get_option_def(optname)
        if value is not None:
            value = _validate(value, optdict, optname)
        if action is None:
            action = optdict.get("action", "store")
        if action == "store":
            setattr(self.config, self.option_attrname(optname, optdict), value)
        elif action in {"store_true", "count"}:
            setattr(self.config, self.option_attrname(optname, optdict), value)
        elif action == "store_false":
            setattr(self.config, self.option_attrname(optname, optdict), value)
        elif action == "append":
            optname = self.option_attrname(optname, optdict)
            _list = getattr(self.config, optname, None)
            if _list is None:
                if isinstance(value, (list, tuple)):
                    _list = value
                elif value is not None:
                    _list = [value]
                setattr(self.config, optname, _list)
            elif isinstance(_list, tuple):
                setattr(self.config, optname, _list + (value,))
            else:
                _list.append(value)
        elif (
            action == "callback"
            or (not isinstance(action, str))
            and issubclass(action, _CallbackAction)
        ):
            return
        else:
            raise UnsupportedAction(action)

    def get_option_def(self, opt):
        """Return the dictionary defining an option given its name."""
        assert self.options
        for option in self.options:
            if option[0] == opt:
                return option[1]
        raise optparse.OptionError(
            f"no such option {opt} in section {self.name!r}", opt
        )

    def options_by_section(self):
        """Return an iterator on options grouped by section.

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
            yield optname, optdict, self.option_value(optname)
