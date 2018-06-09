# -*- coding: utf-8 -*-
# Copyright (c) 2006-2010, 2012-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2008 pyves@crater.logilab.fr <pyves@crater.logilab.fr>
# Copyright (c) 2010 Julien Jehannet <julien.jehannet@logilab.fr>
# Copyright (c) 2013 Google, Inc.
# Copyright (c) 2013 John McGehee <jmcgehee@altera.com>
# Copyright (c) 2014-2018 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2015 John Kirkham <jakirkham@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Erik <erik.eriksson@yahoo.com>
# Copyright (c) 2016 Alexander Todorov <atodorov@otb.bg>
# Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
# Copyright (c) 2017-2018 Ville Skyttä <ville.skytta@iki.fi>
# Copyright (c) 2017 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2017 ahirnish <ahirnish@gmail.com>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2018 Bryce Guinta <bryce.paul.guinta@gmail.com>
# Copyright (c) 2018 ssolanki <sushobhitsolanki@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Anthony Sottile <asottile@umich.edu>
# Copyright (c) 2018 Gary Tyler McLeod <mail@garytyler.com>
# Copyright (c) 2018 Konstantin <Github@pheanex.de>
# Copyright (c) 2018 Nick Drozd <nicholasdrozd@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""utilities for Pylint configuration :

* pylintrc
* pylint.d (PYLINTHOME)
"""
from __future__ import print_function

import abc
import argparse
import collections
import os
import pickle
import re
import sys
import textwrap

import configparser

from pylint import exceptions, utils


USER_HOME = os.path.expanduser('~')
if 'PYLINTHOME' in os.environ:
    PYLINT_HOME = os.environ['PYLINTHOME']
    if USER_HOME == '~':
        USER_HOME = os.path.dirname(PYLINT_HOME)
elif USER_HOME == '~':
    PYLINT_HOME = ".pylint.d"
else:
    PYLINT_HOME = os.path.join(USER_HOME, '.pylint.d')


def _get_pdata_path(base_name, recurs):
    base_name = base_name.replace(os.sep, '_')
    return os.path.join(PYLINT_HOME, "%s%s%s"%(base_name, recurs, '.stats'))


def load_results(base):
    data_file = _get_pdata_path(base, 1)
    try:
        with open(data_file, _PICK_LOAD) as stream:
            return pickle.load(stream)
    except Exception: # pylint: disable=broad-except
        return {}

if sys.version_info < (3, 0):
    _PICK_DUMP, _PICK_LOAD = 'w', 'r'
else:
    _PICK_DUMP, _PICK_LOAD = 'wb', 'rb'

def save_results(results, base):
    if not os.path.exists(PYLINT_HOME):
        try:
            os.mkdir(PYLINT_HOME)
        except OSError:
            print('Unable to create directory %s' % PYLINT_HOME, file=sys.stderr)
    data_file = _get_pdata_path(base, 1)
    try:
        with open(data_file, _PICK_DUMP) as stream:
            pickle.dump(results, stream)
    except (IOError, OSError) as ex:
        print('Unable to create file %s: %s' % (data_file, ex), file=sys.stderr)


def find_pylintrc_in(search_dir):
    """Find a pylintrc file in the given directory.

    :param search_dir: The directory to search.
    :type search_dir: str

    :returns: The path to the pylintrc file, if found. Otherwise None.
    :rtype: str or None
    """
    path = None

    search_dir = os.path.expanduser(search_dir)
    if os.path.isfile(os.path.join(search_dir, 'pylintrc')):
        path = os.path.join(search_dir, 'pylintrc')
    elif os.path.isfile(os.path.join(search_dir, '.pylintrc')):
        path = os.path.join(search_dir, '.pylintrc')

    return path


def find_nearby_pylintrc(search_dir=''):
    """Search for the nearest pylint rc file.

    :param search_dir: The directory to search.
    :type search_dir: str

    :returns: The absolute path to the pylintrc file, if found.
        Otherwise None
    :rtype: str or None
    """
    search_dir = os.path.expanduser(search_dir)
    path = find_pylintrc_in(search_dir)

    if not path:
        for cur_dir in utils.walk_up(search_dir):
            if not os.path.isfile(os.path.join(cur_dir, '__init__.py')):
                break
            path = find_pylintrc_in(cur_dir)
            if path:
                break

    if path:
        path = os.path.abspath(path)

    return path


def find_global_pylintrc():
    """Search for the global pylintrc file.

    :returns: The absolute path to the pylintrc file, if found. Otherwise None.
    :rtype: str or None
    """
    pylintrc = None

    if 'PYLINTRC' in os.environ and os.path.isfile(os.environ['PYLINTRC']):
        pylintrc = os.environ['PYLINTRC']
    else:
        search_dirs = (
            '~', '/root', os.path.join('~', '.config'), '/etc/pylintrc',
        )
        for search_dir in search_dirs:
            path = find_pylintrc_in(search_dir)
            if path:
                pylintrc = path
                break

    return pylintrc


def find_pylintrc():
    """Search for a pylintrc file.
    The locations searched are, in order:
    - The current directory
    - Each parent directory that contains a __init__.py file
    - The value of the `PYLINTRC` environment variable
    - The current user's home directory
    - The `.config` folder in the current user's home directory
    - /etc/pylintrc

    :returns: The path to the pylintrc file, or None if one was not found.
    :rtype: str or None
    """
    # TODO: Find nearby pylintrc files as well
    #return find_nearby_pylintrc() or find_global_pylintrc()
    return find_global_pylintrc()


PYLINTRC = find_pylintrc()

ENV_HELP = '''
The following environment variables are used:
    * PYLINTHOME
    Path to the directory where persistent data for the run will be stored. If
not found, it defaults to ~/.pylint.d/ or .pylint.d (in the current working
directory).
    * PYLINTRC
    Path to the configuration file. See the documentation for the method used
to search for configuration file.
''' % globals()


class UnsupportedAction(Exception):
    """raised by set_option when it doesn't know what to do for an action"""


def _regexp_csv_validator(value):
    return [re.compile(val) for val in utils._check_csv(value)]

def _yn_validator(value):
    if value in ('y', 'yes'):
        return True
    if value in ('n', 'no'):
        return False
    msg = "invalid yn value %r, should be in (y, yes, n, no)"
    raise argparse.ArgumentTypeError(msg % (value,))


def _non_empty_string_validator(value):
    if not value:
        msg = "indent string can't be empty."
        raise argparse.ArgumentTypeError(msg)
    return utils._unquote(value)


VALIDATORS = {
    'string': utils._unquote,
    'int': int,
    'regexp': re.compile,
    'regexp_csv': _regexp_csv_validator,
    'csv': utils._check_csv,
    'yn': _yn_validator,
    'non_empty_string': _non_empty_string_validator,
}


UNVALIDATORS = {
    'string': str,
    'int': str,
    'regexp': lambda value: getattr(value, 'pattern', value),
    'regexp_csv': (lambda value: ','.join(r.pattern for r in value)),
    'csv': (lambda value: ','.join(value)),
    'yn': (lambda value: 'y' if value else 'n'),
    'non_empty_string': str,
}


OptionDefinition = collections.namedtuple(
    'OptionDefinition', ['name', 'definition']
)


class Configuration(object):
    def __init__(self):
        self._option_definitions = {}

    def add_option(self, option_definition):
        name, definition = option_definition
        if name in self._option_definitions:
            raise exceptions.ConfigurationError('Option "{0}" already exists.')

        self._option_definitions[name] = definition
        if 'default' in definition:
            dest = definition.get('dest', name)
            self.set_option(dest, definition['default'])

    def add_options(self, option_definitions):
        for option_definition in option_definitions:
            self.add_option(option_definition)

    def set_option(self, option, value):
        option = option.replace('-', '_')
        setattr(self, option, value)

    def copy(self):
        result = self.__class__()
        result.add_options(self._option_definitions.items())

        for option in self._option_definitions:
            value = getattr(self, option)
            setattr(result, option, value)

        return result

    def __add__(self, other):
        result = self.copy()
        result += other
        return result

    def __iadd__(self, other):
        self._option_definitions.update(other._option_definitions)

        for option in other._option_definitions:
            option = option.replace('-', '_')
            value = getattr(other, option)
            setattr(self, option, value)

        return self


class ConfigurationStore(object):
    def __init__(self, global_config):
        """A class to store configuration objects for many paths.

        :param global_config: The global configuration object.
        :type global_config: Configuration
        """
        self.global_config = global_config

        self._store = {}
        self._cache = {}

    def add_config_for(self, path, config):
        """Add a configuration object to the store.

        :param path: The path to add the config for.
        :type path: str
        :param config: The config object for the given path.
        :type config: Configuration
        """
        path = os.path.expanduser(path)
        path = os.path.abspath(path)

        self._store[path] = config
        self._cache = {}

    def _get_parent_configs(self, path):
        """Get the config objects for all parent directories.

        :param path: The absolute path to get the parent configs for.
        :type path: str

        :returns: The config objects for all parent directories.
        :rtype: generator(Configuration)
        """
        for cfg_dir in utils.walk_up(path):
            if cfg_dir in self._cache:
                yield self._cache[cfg_dir]
                break
            elif cfg_dir in self._store:
                yield self._store[cfg_dir]

    def get_config_for(self, path):
        """Get the configuration object for a file or directory.
        This will merge the global config with all of the config objects from
        the root directory to the given path.

        :param path: The file or directory to the get configuration object for.
        :type path: str

        :returns: The configuration object for the given file or directory.
        :rtype: Configuration
        """
        # TODO: Until we turn on local pylintrc searching,
        # this is always going to be the global config
        return self.global_config

        path = os.path.expanduser(path)
        path = os.path.abspath(path)

        config = self._cache.get(path)

        if not config:
            config = self.global_config.copy()

            parent_configs = self._get_parent_configs(path)
            for parent_config in reversed(list(parent_configs)):
                config += parent_config

            self._cache['path'] = config

        return config

    def __getitem__(self, path):
        return self.get_config_for(path)

    def __setitem__(self, path, config):
        return self.add_config_for(path, config)


class ConfigParser(metaclass=abc.ABCMeta):
    def __init__(self):
        self._option_definitions = {}
        self._option_groups = set()

    def add_option_definitions(self, option_definitions):
        self._option_definitions.update(option_definitions)

        for _, definition_dict in option_definitions:
            try:
                group = definition_dict['group'].upper()
            except KeyError:
                continue
            else:
                self._option_groups.add(group)

    def add_option_definition(self, option_definition):
        self.add_option_definitions([option_definition])

    @abc.abstractmethod
    def parse(self, to_parse, config):
        """Parse the given object into the config object.

        :param to_parse: The object to parse.
        :type to_parse: object
        :param config: The config object to parse into.
        :type config: Configuration
        """


class CLIParser(ConfigParser):
    def __init__(self, usage=''):
        super(CLIParser, self).__init__()

        self._parser = LongHelpArgumentParser(
            usage=usage.replace("%prog", "%(prog)s"),
            # Only set the arguments that are specified.
            argument_default=argparse.SUPPRESS
        )
        # TODO: Let this be definable elsewhere
        self._parser.add_argument('module_or_package', nargs=argparse.REMAINDER)

    def add_option_definitions(self, option_definitions):
        self._option_definitions.update(option_definitions)
        option_groups = collections.defaultdict(list)

        for option, definition in option_definitions:
            group, args, kwargs = self._convert_definition(option, definition)
            option_groups[group].append((args, kwargs))

        for args, kwargs in option_groups['MASTER']:
            self._parser.add_argument(*args, **kwargs)

        del option_groups['MASTER']

        for group, arguments in option_groups.items():
            self._option_groups.add(group)
            group = self._parser.add_argument_group(group.title())
            for args, kwargs in arguments:
                group.add_argument(*args, **kwargs)

    @staticmethod
    def _convert_definition(option, definition):
        """Convert an option definition to a set of arguments for add_argument.

        :param option: The name of the option
        :type option: str
        :param definition: The argument definition to convert.
        :type definition: dict

        :returns: A tuple of the group to add the argument to,
            plus the args and kwargs for :func:`ArgumentParser.add_argument`.
        :rtype: tuple(str, list, dict)

        :raises ConfigurationError: When the definition is invalid.
        """
        args = []

        if 'short' in definition:
            args.append('-{0}'.format(definition['short']))

        args.append('--{0}'.format(option))

        copy_keys = (
            'action', 'default', 'dest', 'help', 'metavar', 'level', 'version')
        kwargs = {k: definition[k] for k in copy_keys if k in definition}

        if 'type' in definition:
            if definition['type'] in VALIDATORS:
                kwargs['type'] = VALIDATORS[definition['type']]
            elif definition['type'] in ('choice', 'multiple_choice'):
                if 'choices' not in definition:
                    msg = 'No choice list given for option "{0}" of type "choice".'
                    msg = msg.format(option)
                    raise exceptions.ConfigurationError(msg)

                if definition['type'] == 'multiple_choice':
                    kwargs['type'] = VALIDATORS['csv']

                kwargs['choices'] = definition['choices']
            else:
                msg = 'Unsupported type "{0}"'.format(definition['type'])
                raise exception.ConfigurationError(msg)

        if definition.get('hide'):
            kwargs['help'] = argparse.SUPPRESS

        group = definition.get('group', 'MASTER').upper()
        return group, args, kwargs

    def parse(self, to_parse, config):
        """Parse the command line arguments into the given config object.

        :param to_parse: The command line arguments to parse.
        :type to_parse: list(str)
        :param config: The config object to parse the command line into.
        :type config: Configuration
        """
        self._parser.parse_args(to_parse, config)

    def preprocess(self, argv, *options):
        """Do some guess work to get a value for the specified option.

        :param argv: The command line arguments to parse.
        :type argv: list(str)
        :param options: The names of the options to look for.
        :type options: str

        :returns: A config with the processed options.
        :rtype: Configuration
        """
        config = Configuration()
        config.add_options(self._option_definitions.items())

        args = self._parser.parse_known_args(argv)[0]
        for option in options:
            option = option.replace('-', '_')
            config.set_option(option, getattr(args, option, None))

        return config

    def add_help_section(self, title, description, level=0):
        """Add an extra help section to the help message.

        :param title: The title of the section.
            This is included as part of the help message.
        :type title: str
        :param description: The description of the help section.
        :type description: str
        :param level: The minimum level of help needed to include this
            in the help message.
        :type level: int
        """
        self._parser.add_argument_group(title, description, level=level)


class FileParser(ConfigParser, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, to_parse, config):
        pass


def make_commenter(description):
    """Make a function to add comments from re.sub."""
    def make_comment(match):
        """Make the replacement string including commented desciption."""
        comment = '\n'.join(
            '# {}'.format(line) for line in textwrap.wrap(description))
        return match.expand(r'{}\n\g<0>'.format(comment))
    return make_comment


def make_commented_config_text(option_definitions, config_text):
    """Make config ini text with descriptions added as comments."""
    for name, definition in option_definitions.items():
        config_text = re.sub(
            r'^{}[ =]'.format(re.escape(name)),
            make_commenter(definition['help']),
            config_text,
            flags=re.MULTILINE
        )
    return config_text


class IniFileParser(FileParser):
    """Parses a config files into config objects."""

    def __init__(self):
        super(IniFileParser, self).__init__()
        self._parser = configparser.ConfigParser(
            inline_comment_prefixes=('#', ';'),
            default_section='MASTER',
        )

    def add_option_definitions(self, option_definitions):
        self._option_definitions.update(option_definitions)
        for option, definition in option_definitions:
            group, default = self._convert_definition(option, definition)

            if group != self._parser.default_section:
                try:
                    self._parser.add_section(group)
                except configparser.DuplicateSectionError:
                    pass
                else:
                    self._option_groups.add(group)

            if default is not None:
                self._parser['MASTER'].update(default)

    @staticmethod
    def _convert_definition(option, definition):
        """Convert an option definition to a set of arguments for the parser.

        :param option: The name of the option.
        :type option: str
        :param definition: The argument definition to convert.
        :type definition: dict

        :returns: The converted definition.
        :rtype: tuple(str, dict)
        """
        default = None
        if definition.get('default'):
            unvalidator = UNVALIDATORS.get(definition.get('type'), str)
            default_value = unvalidator(definition['default'])
            default = {option: default_value}

        group = definition.get('group', 'MASTER').upper()
        return group, default

    def parse(self, to_parse, config):
        self._parser.read(to_parse)

        for section in self._parser.sections():
            # Normalise the section titles
            if not section.isupper():
                new_section = section.upper()
                for option, value in self._parser.items(section):
                    self._parser.set(new_section, option, value)
                self._parser.remove_section(section)
                section = section.upper()

            for option, value in self._parser.items(section):
                if isinstance(value, str):
                    definition = self._option_definitions.get(option, {})
                    type_ = definition.get('type')
                    validator = VALIDATORS.get(type_, lambda x: x)
                    value = validator(value)
                config.set_option(option, value)

    def write(self, stream=sys.stdout):
        with six.StringIO() as temp_stream:
            self._parser.write(temp_stream)
            config_text = temp_stream.getvalue()
        config_text = make_commented_config_text(
            self._option_definitions, config_text)
        stream.write(config_text)


class LongHelpFormatter(argparse.HelpFormatter):
    output_level = None

    def add_argument(self, action):
        if action.level <= self.output_level:
            super(LongHelpFormatter, self).add_argument(action)

    def add_usage(self, usage, actions, groups, prefix=None):
        actions = [action for action in actions if action.level <= self.output_level]
        super(LongHelpFormatter, self).add_usage(
            usage, actions, groups, prefix,
        )


class LongHelpAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help=None):
        super(LongHelpAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help,
        )
        self.level = 0

    @staticmethod
    def _parse_option_string(option_string):
        level = 0
        if option_string:
            level = option_string.count('l-') or option_string.count('long-')
        return level

    @staticmethod
    def build_add_args(level, prefix_chars='-'):
        default_prefix = '-' if '-' in prefix_chars else prefix_chars[0]
        return (
            default_prefix + '-'.join(['l'] * level) + '-h',
            default_prefix * 2 + '-'.join(['long'] * level) + '-help',
        )

    def __call__(self, parser, namespace, values, option_string=None):
        level = self._parse_option_string(option_string)
        parser.print_help(level=level)
        parser.exit()


class LongHelpArgumentGroup(argparse._ArgumentGroup):
    def __init__(self, *args, level=0, **kwargs):
        super(LongHelpArgumentGroup, self).__init__(*args, **kwargs)
        self.level = level

    def add_argument(self, *args, **kwargs):
        """See :func:`argparse.ArgumentParser.add_argument`.

        Patches in the level to each created action instance.

        :returns: The created action.
        :rtype: argparse.Action
        """
        level = kwargs.pop('level', 0)
        action = super(LongHelpArgumentGroup, self).add_argument(*args, **kwargs)
        action.level = level
        return action


class LongHelpArgumentParser(argparse.ArgumentParser):
    def __init__(self, formatter_class=LongHelpFormatter, **kwargs):
        self._max_level = 0
        super(LongHelpArgumentParser, self).__init__(
            formatter_class=formatter_class, **kwargs
        )

    # Stop ArgumentParser __init__ adding the wrong help formatter
    def register(self, registry_name, value, object):
        if registry_name == 'action' and value == 'help':
            object = LongHelpAction

        super(LongHelpArgumentParser, self).register(
            registry_name, value, object
        )

    def _add_help_levels(self):
        level = max(action.level for action in self._actions)
        if level > self._max_level and self.add_help:
            for new_level in range(self._max_level + 1, level + 1):
                action = super(LongHelpArgumentParser, self).add_argument(
                    *LongHelpAction.build_add_args(new_level, self.prefix_chars),
                    action='help',
                    default=argparse.SUPPRESS,
                    help=('show this {0} verbose help message and exit'.format(
                        ' '.join(['really'] * (new_level - 1))
                    ))
                )
                action.level = 0
            self._max_level = level

    def parse_known_args(self, *args, **kwargs):
        self._add_help_levels()
        return super(LongHelpArgumentParser, self).parse_known_args(
            *args, **kwargs
        )

    def add_argument(self, *args, **kwargs):
        """See :func:`argparse.ArgumentParser.add_argument`.

        Patches in the level to each created action instance.

        :returns: The created action.
        :rtype: argparse.Action
        """
        level = kwargs.pop('level', 0)
        action = super(LongHelpArgumentParser, self).add_argument(*args, **kwargs)
        action.level = level
        return action

    def add_argument_group(self, *args, **kwargs):
        group = LongHelpArgumentGroup(self, *args, **kwargs)
        self._action_groups.append(group)
        return group

    # These methods use yucky way of passing the level to the formatter class
    # without having to rely on argparse implementation details.
    def format_usage(self, level=0):
        if hasattr(self.formatter_class, 'output_level'):
            if self.formatter_class.output_level is None:
                self.formatter_class.output_level = level
        return super(LongHelpArgumentParser, self).format_usage()

    def format_help(self, level=0):
        if hasattr(self.formatter_class, 'output_level'):
            if self.formatter_class.output_level is None:
                self.formatter_class.output_level = level
            else:
                level = self.formatter_class.output_level

        # Unfortunately there's no way of publicly accessing the groups or
        # an easy way of overriding format_help without using protected methods.
        old_action_groups = self._action_groups
        try:
            self._action_groups = [group for group in self._action_groups if group.level <= level]
            result = super(LongHelpArgumentParser, self).format_help()
        finally:
            self._action_groups = old_action_groups

        return result

    def print_usage(self, file=None, level=0):
        if hasattr(self.formatter_class, 'output_level'):
            if self.formatter_class.output_level is None:
                self.formatter_class.output_level = level
        super(LongHelpArgumentParser, self).print_usage(file)

    def print_help(self, file=None, level=0):
        if hasattr(self.formatter_class, 'output_level'):
            if self.formatter_class.output_level is None:
                self.formatter_class.output_level = level
        super(LongHelpArgumentParser, self).print_help(file)
