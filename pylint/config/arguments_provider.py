# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Arguments provider class used to expose options."""


import optparse  # pylint: disable=deprecated-module
import warnings
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

from pylint.config.arguments_manager import _ArgumentsManager
from pylint.config.callback_actions import _CallbackAction
from pylint.config.option import _validate
from pylint.typing import OptionDict, Options


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
        self._config = optparse.Values()
        self.level = 0

    @property
    def config(self) -> optparse.Values:
        warnings.warn(
            "The checker-specific config attribute has been deprecated. Please use "
            "'linter.config' to access the global configuration object.",
            DeprecationWarning,
        )
        return self._config

    def load_defaults(self) -> None:
        """DEPRECATED: Initialize the provider using default values."""
        warnings.warn(
            "load_defaults has been deprecated. Option groups should be "
            "registered by initializing an ArgumentsProvider. "
            "This automatically registers the group on the ArgumentsManager.",
            DeprecationWarning,
        )
        for opt, optdict in self.options:
            action = optdict.get("action")
            if action != "callback":
                # callback action have no default
                if optdict is None:
                    with warnings.catch_warnings():
                        warnings.filterwarnings("ignore", category=DeprecationWarning)
                        optdict = self.get_option_def(opt)
                default = optdict.get("default")
                self.set_option(opt, default, action, optdict)

    def option_attrname(self, opt: str, optdict: Optional[OptionDict] = None) -> str:
        """DEPRECATED: Get the config attribute corresponding to opt."""
        warnings.warn(
            "option_attrname has been deprecated. It will be removed "
            "in a future release.",
            DeprecationWarning,
        )
        if optdict is None:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                optdict = self.get_option_def(opt)
        return optdict.get("dest", opt.replace("-", "_"))  # type: ignore[return-value]

    def option_value(self, opt: str) -> Any:
        """DEPRECATED: Get the current value for the given option."""
        warnings.warn(
            "option_value has been deprecated. It will be removed "
            "in a future release.",
            DeprecationWarning,
        )
        return getattr(self._arguments_manager.namespace, opt.replace("-", "_"), None)

    # pylint: disable-next=fixme
    # TODO: Optparse: Refactor and deprecate set_option
    def set_option(self, optname, value, action=None, optdict=None):
        """Method called to set an option (registered in the options list)."""
        if optdict is None:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                optdict = self.get_option_def(optname)
        if value is not None:
            value = _validate(value, optdict, optname)
        if action is None:
            action = optdict.get("action", "store")
        if action == "store":
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                setattr(self.config, self.option_attrname(optname, optdict), value)
        elif action in {"store_true", "count"}:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                setattr(self.config, self.option_attrname(optname, optdict), value)
        elif action == "store_false":
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                setattr(self.config, self.option_attrname(optname, optdict), value)
        elif action == "append":
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
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
        elif action == "extend":
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
                _list.extend(value)
        elif (
            action == "callback"
            or (not isinstance(action, str))
            and issubclass(action, _CallbackAction)
        ):
            return
        else:
            raise UnsupportedAction(action)

    def get_option_def(self, opt: str) -> OptionDict:
        """DEPRECATED: Return the dictionary defining an option given its name.

        :raises OptionError: If the option isn't found.
        """
        warnings.warn(
            "get_option_def has been deprecated. It will be removed "
            "in a future release.",
            DeprecationWarning,
        )
        assert self.options
        for option in self.options:
            if option[0] == opt:
                return option[1]
        raise optparse.OptionError(
            f"no such option {opt} in section {self.name!r}", opt  # type: ignore[arg-type]
        )

    def options_by_section(
        self,
    ) -> Iterator[
        Tuple[
            Optional[str],
            Union[
                Dict[str, List[Tuple[str, OptionDict, Any]]],
                List[Tuple[str, OptionDict, Any]],
            ],
        ]
    ]:
        """DEPRECATED: Return an iterator on options grouped by section.

        (section, [list of (optname, optdict, optvalue)])
        """
        warnings.warn(
            "options_by_section has been deprecated. It will be removed "
            "in a future release.",
            DeprecationWarning,
        )
        sections: Dict[str, List[Tuple[str, OptionDict, Any]]] = {}
        for optname, optdict in self.options:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                sections.setdefault(optdict.get("group"), []).append(  # type: ignore[arg-type]
                    (optname, optdict, self.option_value(optname))
                )
        if None in sections:
            yield None, sections.pop(None)  # type: ignore[call-overload]
        for section, options in sorted(sections.items()):
            yield section.upper(), options

    def options_and_values(
        self, options: Optional[Options] = None
    ) -> Iterator[Tuple[str, OptionDict, Any]]:
        """DEPRECATED."""
        warnings.warn(
            "options_and_values has been deprecated. It will be removed "
            "in a future release.",
            DeprecationWarning,
        )
        if options is None:
            options = self.options
        for optname, optdict in options:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                yield optname, optdict, self.option_value(optname)
