# -*- coding: utf-8 -*-
# Copyright (c) 2006-2010, 2012-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2008 pyves@crater.logilab.fr <pyves@crater.logilab.fr>
# Copyright (c) 2010 Julien Jehannet <julien.jehannet@logilab.fr>
# Copyright (c) 2013 Google, Inc.
# Copyright (c) 2013 John McGehee <jmcgehee@altera.com>
# Copyright (c) 2014-2016 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Aru Sahni <arusahni@gmail.com>
# Copyright (c) 2015 John Kirkham <jakirkham@gmail.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Erik <erik.eriksson@yahoo.com>
# Copyright (c) 2016 Alexander Todorov <atodorov@otb.bg>
# Copyright (c) 2016 Moises Lopez <moylop260@vauxoo.com>
# Copyright (c) 2017 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2017 ahirnish <ahirnish@gmail.com>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>
# Copyright (c) 2017 Ville Skyttä <ville.skytta@iki.fi>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""utilities for Pylint configuration :

* pylintrc
* pylint.d (PYLINTHOME)
"""
from __future__ import print_function

import abc
import argparse
import contextlib
import collections
import copy
import functools
import io
import optparse
import os
import pickle
import re
import sys
import time

import configparser
import six
from six.moves import range

from pylint import utils


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


# TODO: Put into utils
def walk_up(from_dir):
    """Walk up a directory tree
    :param from_dir: The directory to walk up from.
        This directory is included in the output.
    :type from_dir: str
    :returns: Each parent directory
    :rtype: generator(str)
    """
    cur_dir = None
    new_dir = os.path.expanduser(from_dir)
    new_dir = os.path.abspath(new_dir)

    # The parent of the root directory is the root directory.
    # Once we have reached it, we are done.
    while cur_dir != new_dir:
        cur_dir = new_dir
        yield cur_dir
        new_dir = os.path.abspath(os.path.join(cur_dir, os.pardir))


def find_pylintrc_in(search_dir):
    """Find a pylintrc file in the given directory.
    :param search_dir: The directory to search.
    :type search_dir: str
    :returns: The path to the pylintrc file, if found.
        Otherwise None.
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
        for search_dir in walk_up(search_dir):
            if not os.path.isfile(os.path.join(search_dir, '__init__.py')):
                break
            path = find_pylintrc_in(search_dir)
            if path:
                break

    if path:
        path = os.path.abspath(path)

    return path


def find_global_pylintrc():
    """Search for the global pylintrc file.
    :returns: The absolute path to the pylintrc file, if found.
        Otherwise None.
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
    :returns: The path to the pylintrc file,
        or None if one was not found.
    :rtype: str or None
    """
    # TODO: Find nearby pylintrc files as well
    #return find_nearby_pylintrc() or find_global_pylintrc()
    return find_global_pylintrc()


PYLINTRC = find_pylintrc()

ENV_HELP = '''
The following environment variables are used:
    * PYLINTHOME
    Path to the directory where the persistent for the run will be stored. If
not found, it defaults to ~/.pylint.d/ or .pylint.d (in the current working
directory).
    * PYLINTRC
    Path to the configuration file. See the documentation for the method used
to search for configuration file.
''' % globals()


class UnsupportedAction(Exception):
    """raised by set_option when it doesn't know what to do for an action"""


def _multiple_choice_validator(choices, name, value):
    values = utils._check_csv(value)
    for csv_value in values:
        if csv_value not in choices:
            msg = "option %s: invalid value: %r, should be in %s"
            raise optparse.OptionValueError(msg % (name, csv_value, choices))
    return values


def _choice_validator(choices, name, value):
    if value not in choices:
        msg = "option %s: invalid value: %r, should be in %s"
        raise optparse.OptionValueError(msg % (name, value, choices))
    return value

# pylint: disable=unused-argument
def _csv_validator(_, name, value):
    return utils._check_csv(value)


# pylint: disable=unused-argument
def _regexp_validator(_, name, value):
    if hasattr(value, 'pattern'):
        return value
    return re.compile(value)

# pylint: disable=unused-argument
def _regexp_csv_validator(_, name, value):
    return [_regexp_validator(_, name, val) for val in _csv_validator(_, name, value)]

def _yn_validator(opt, _, value):
    if isinstance(value, int):
        return bool(value)
    if value in ('y', 'yes'):
        return True
    if value in ('n', 'no'):
        return False
    msg = "option %s: invalid yn value %r, should be in (y, yes, n, no)"
    raise optparse.OptionValueError(msg % (opt, value))


def _non_empty_string_validator(opt, _, value):
    if not value:
        msg = "indent string can't be empty."
        raise optparse.OptionValueError(msg)
    return utils._unquote(value)


VALIDATORS = {
    'string': utils._unquote,
    'int': int,
    'regexp': re.compile,
    'regexp_csv': _regexp_csv_validator,
    'csv': _csv_validator,
    'yn': _yn_validator,
    'choice': lambda opt, name, value: _choice_validator(opt['choices'], name, value),
    'multiple_choice': lambda opt, name, value: _multiple_choice_validator(opt['choices'],
                                                                           name, value),
    'non_empty_string': _non_empty_string_validator,
}

def _call_validator(opttype, optdict, option, value):
    if opttype not in VALIDATORS:
        raise Exception('Unsupported type "%s"' % opttype)
    try:
        return VALIDATORS[opttype](optdict, option, value)
    except TypeError:
        try:
            return VALIDATORS[opttype](value)
        except Exception:
            raise optparse.OptionValueError('%s value (%r) should be of type %s' %
                                            (option, value, opttype))


def _validate(value, optdict, name=''):
    """return a validated value for an option according to its type

    optional argument name is only used for error message formatting
    """
    try:
        _type = optdict['type']
    except KeyError:
        # FIXME
        return value
    return _call_validator(_type, optdict, name, value)


def _level_options(group, outputlevel):
    return [option for option in group.option_list
            if (getattr(option, 'level', 0) or 0) <= outputlevel
            and option.help is not optparse.SUPPRESS_HELP]


def _expand_default(self, option):
    """Patch OptionParser.expand_default with custom behaviour

    This will handle defaults to avoid overriding values in the
    configuration file.
    """
    if self.parser is None or not self.default_tag:
        return option.help
    optname = option._long_opts[0][2:]
    try:
        provider = self.parser.options_manager._all_options[optname]
    except KeyError:
        value = None
    else:
        optdict = provider.get_option_def(optname)
        optname = provider.option_attrname(optname, optdict)
        value = getattr(provider.config, optname, optdict)
        value = utils._format_option_value(optdict, value)
    if value is optparse.NO_DEFAULT or not value:
        value = self.NO_DEFAULT_VALUE
    return option.help.replace(self.default_tag, str(value))


@contextlib.contextmanager
def _patch_optparse():
    orig_default = optparse.HelpFormatter
    try:
        optparse.HelpFormatter.expand_default = _expand_default
        yield
    finally:
        optparse.HelpFormatter.expand_default = orig_default


def _multiple_choices_validating_option(opt, name, value):
    return _multiple_choice_validator(opt.choices, name, value)


# pylint: disable=no-member
class Option(optparse.Option):
    TYPES = optparse.Option.TYPES + ('regexp', 'regexp_csv', 'csv', 'yn',
                                     'multiple_choice',
                                     'non_empty_string')
    ATTRS = optparse.Option.ATTRS + ['hide', 'level']
    TYPE_CHECKER = copy.copy(optparse.Option.TYPE_CHECKER)
    TYPE_CHECKER['regexp'] = _regexp_validator
    TYPE_CHECKER['regexp_csv'] = _regexp_csv_validator
    TYPE_CHECKER['csv'] = _csv_validator
    TYPE_CHECKER['yn'] = _yn_validator
    TYPE_CHECKER['multiple_choice'] = _multiple_choices_validating_option
    TYPE_CHECKER['non_empty_string'] = _non_empty_string_validator

    def __init__(self, *opts, **attrs):
        optparse.Option.__init__(self, *opts, **attrs)
        if hasattr(self, "hide") and self.hide:
            self.help = optparse.SUPPRESS_HELP

    def _check_choice(self):
        if self.type in ("choice", "multiple_choice"):
            if self.choices is None:
                raise optparse.OptionError(
                    "must supply a list of choices for type 'choice'", self)
            elif not isinstance(self.choices, (tuple, list)):
                raise optparse.OptionError(
                    "choices must be a list of strings ('%s' supplied)"
                    % str(type(self.choices)).split("'")[1], self)
        elif self.choices is not None:
            raise optparse.OptionError(
                "must not supply choices for type %r" % self.type, self)
    optparse.Option.CHECK_METHODS[2] = _check_choice

    def process(self, opt, value, values, parser):
        # First, convert the value(s) to the right type.  Howl if any
        # value(s) are bogus.
        value = self.convert_value(opt, value)
        if self.type == 'named':
            existent = getattr(values, self.dest)
            if existent:
                existent.update(value)
                value = existent
        # And then take whatever action is expected of us.
        # This is a separate method to make life easier for
        # subclasses to add new actions.
        return self.take_action(
            self.action, self.dest, opt, value, values, parser)


class OptionParser(optparse.OptionParser):

    def __init__(self, option_class, *args, **kwargs):
        optparse.OptionParser.__init__(self, option_class=Option, *args, **kwargs)

    def format_option_help(self, formatter=None):
        if formatter is None:
            formatter = self.formatter
        outputlevel = getattr(formatter, 'output_level', 0)
        formatter.store_option_strings(self)
        result = []
        result.append(formatter.format_heading("Options"))
        formatter.indent()
        if self.option_list:
            result.append(optparse.OptionContainer.format_option_help(self, formatter))
            result.append("\n")
        for group in self.option_groups:
            if group.level <= outputlevel and (
                    group.description or _level_options(group, outputlevel)):
                result.append(group.format_help(formatter))
                result.append("\n")
        formatter.dedent()
        # Drop the last "\n", or the header if no options or option groups:
        return "".join(result[:-1])

    def _match_long_opt(self, opt):
        """Disable abbreviations."""
        if opt not in self._long_opt:
            raise optparse.BadOptionError(opt)
        return opt


# pylint: disable=abstract-method; by design?
class _ManHelpFormatter(optparse.HelpFormatter):

    def __init__(self, indent_increment=0, max_help_position=24,
                 width=79, short_first=0):
        optparse.HelpFormatter.__init__(
            self, indent_increment, max_help_position, width, short_first)

    def format_heading(self, heading):
        return '.SH %s\n' % heading.upper()

    def format_description(self, description):
        return description

    def format_option(self, option):
        try:
            optstring = option.option_strings
        except AttributeError:
            optstring = self.format_option_strings(option)
        if option.help:
            help_text = self.expand_default(option)
            help_string = ' '.join([l.strip() for l in help_text.splitlines()])
        else:
            help_string = ''
        return '''.IP "%s"
%s
''' % (optstring, help_string)

    def format_head(self, optparser, pkginfo, section=1):
        long_desc = ""
        try:
            pgm = optparser._get_prog_name()
        except AttributeError:
            # py >= 2.4.X (dunno which X exactly, at least 2)
            pgm = optparser.get_prog_name()
        short_desc = self.format_short_description(pgm, pkginfo.description)
        if hasattr(pkginfo, "long_desc"):
            long_desc = self.format_long_description(pgm, pkginfo.long_desc)
        return '%s\n%s\n%s\n%s' % (self.format_title(pgm, section),
                                   short_desc, self.format_synopsis(pgm),
                                   long_desc)

    @staticmethod
    def format_title(pgm, section):
        date = '-'.join(str(num) for num in time.localtime()[:3])
        return '.TH %s %s "%s" %s' % (pgm, section, date, pgm)

    @staticmethod
    def format_short_description(pgm, short_desc):
        return '''.SH NAME
.B %s
\\- %s
''' % (pgm, short_desc.strip())

    @staticmethod
    def format_synopsis(pgm):
        return '''.SH SYNOPSIS
.B  %s
[
.I OPTIONS
] [
.I <arguments>
]
''' % pgm

    @staticmethod
    def format_long_description(pgm, long_desc):
        long_desc = '\n'.join(line.lstrip()
                              for line in long_desc.splitlines())
        long_desc = long_desc.replace('\n.\n', '\n\n')
        if long_desc.lower().startswith(pgm):
            long_desc = long_desc[len(pgm):]
        return '''.SH DESCRIPTION
.B %s
%s
''' % (pgm, long_desc.strip())

    @staticmethod
    def format_tail(pkginfo):
        tail = '''.SH SEE ALSO
/usr/share/doc/pythonX.Y-%s/

.SH BUGS
Please report bugs on the project\'s mailing list:
%s

.SH AUTHOR
%s <%s>
''' % (getattr(pkginfo, 'debian_name', pkginfo.modname),
       pkginfo.mailinglist, pkginfo.author, pkginfo.author_email)

        if hasattr(pkginfo, "copyright"):
            tail += '''
.SH COPYRIGHT
%s
''' % pkginfo.copyright

        return tail


class OptionsManagerMixIn(object):
    """Handle configuration from both a configuration file and command line options"""

    class CallbackAction(argparse.Action):
        """Doesn't store the value on the config."""
        def __init__(self, *args, nargs=None, **kwargs):
            nargs = nargs or int('metavar' in kwargs)
            super(OptionsManagerMixIn.CallbackAction, self).__init__(
                *args, nargs=nargs, **kwargs
            )

        def __call__(self, parser, namespace, values, option_string):
            # If no value was passed, argparse didn't call the callback via
            # `type`, so we need to do it ourselves.
            if not self.nargs and callable(self.type):
                self.type(self, option_string, values, parser)

    def __init__(self, usage, config_file=None, version=None):
        self.config_file = config_file
        self.reset_parsers(usage, version=version)
        # list of registered options providers
        self.options_providers = []
        # dictionary associating option name to checker
        self._all_options = collections.OrderedDict()
        self._short_options = {}
        self._nocallback_options = {}
        self._mygroups = {}
        # verbosity
        self._maxlevel = 0

    def reset_parsers(self, usage='', version=None):
        # configuration file parser
        self.cfgfile_parser = IniFileParser()
        # command line parser
        self.cmdline_parser = CLIParser(usage)

    def register_options_provider(self, provider, own_group=True):
        """register an options provider"""
        assert provider.priority <= 0, "provider's priority can't be >= 0"
        for i in range(len(self.options_providers)):
            if provider.priority > self.options_providers[i].priority:
                self.options_providers.insert(i, provider)
                break
        else:
            self.options_providers.append(provider)
        non_group_spec_options = [option for option in provider.options
                                  if 'group' not in option[1]]
        groups = getattr(provider, 'option_groups', ())
        if own_group and non_group_spec_options:
            self.add_option_group(provider.name.upper(), provider.__doc__,
                                  non_group_spec_options, provider)
        else:
            for opt, optdict in non_group_spec_options:
                self.add_optik_option(provider, self.cmdline_parser, opt, optdict)
        for gname, gdoc in groups:
            gname = gname.upper()
            goptions = [option for option in provider.options
                        if option[1].get('group', '').upper() == gname]
            self.add_option_group(gname, gdoc, goptions, provider)

    def add_option_group(self, group_name, _, options, provider):
        # add option group to the command line parser
        if group_name in self._mygroups:
            group = self._mygroups[group_name]
        else:
            group = self.cmdline_parser._parser.add_argument_group(
                group_name.capitalize(), level=provider.level,
            )
            self._mygroups[group_name] = group
            # add section to the config file
            if group_name != "DEFAULT":
                try:
                    self.cfgfile_parser._parser.add_section(group_name)
                except configparser.DuplicateSectionError:
                    pass

        # add provider's specific options
        for opt, optdict in options:
            self.add_optik_option(provider, group, opt, optdict)

    def add_optik_option(self, provider, optikcontainer, opt, optdict):
        args, optdict = self.optik_option(provider, opt, optdict)
        if hasattr(optikcontainer, '_parser'):
            optikcontainer = optikcontainer._parser
        if 'group' in optdict:
            optikcontainer = self._mygroups[optdict['group'].upper()]
            del optdict['group']

        # Some sanity checks for things that trip up argparse
        assert not any(' ' in arg for arg in args)
        assert all(optdict.values())
        assert not ('metavar' in optdict and '[' in optdict['metavar'])

        level = optdict.pop('level', 0)
        option = optikcontainer.add_argument(*args, **optdict)
        option.level = level
        self._all_options[opt] = provider
        self._maxlevel = max(self._maxlevel, optdict.get('level', 0))

    def optik_option(self, provider, opt, optdict):
        """get our personal option definition and return a suitable form for
        use with optik/optparse
        """
        # TODO: Changed to work with argparse but this should call
        # self.cmdline_parser.add_argument_definitions and not use callbacks
        optdict = copy.copy(optdict)
        if 'action' in optdict:
            self._nocallback_options[provider] = opt
            if optdict['action'] == 'callback':
                optdict['type'] = optdict['callback']
                optdict['action'] = self.CallbackAction
                del optdict['callback']
        else:
            callback = functools.partial(
                self.cb_set_provider_option, None, '--' + str(opt), parser=None,
            )
            optdict['type'] = callback
            optdict.setdefault('action', 'store')
        # default is handled here and *must not* be given to optik if you
        # want the whole machinery to work
        if 'default' in optdict:
            if ('help' in optdict
                    and optdict.get('default') is not None
                    and optdict['action'] not in ('store_true', 'store_false')):
                default = optdict['default']
                if isinstance(default, (tuple, list)):
                    default = ','.join(str(x) for x in default)
                optdict['help'] += ' [current: {0}]'.format(default)
            del optdict['default']
        args = ['--' + str(opt)]
        if 'short' in optdict:
            self._short_options[optdict['short']] = opt
            args.append('-' + optdict['short'])
            del optdict['short']
        if optdict.get('action') == 'callback':
            optdict['type'] = optdict['callback']
            del optdict['action']
            del optdict['callback']
        if optdict.get('hide'):
            optdict['help'] = argparse.SUPPRESS
            del optdict['hide']
        return args, optdict

    def cb_set_provider_option(self, option, opt, value, parser):
        """optik callback for option setting"""
        if opt.startswith('--'):
            # remove -- on long option
            opt = opt[2:]
        else:
            # short option, get its long equivalent
            opt = self._short_options[opt[1:]]
        # trick since we can't set action='store_true' on options
        if value is None:
            value = 1
        self.global_set_option(opt, value)
        return value

    def global_set_option(self, opt, value):
        """set option on the correct option provider"""
        self._all_options[opt].set_option(opt, value)

    def generate_config(self, stream=None, skipsections=(), encoding=None):
        """write a configuration file according to the current configuration
        into the given stream or stdout
        """
        options_by_section = {}
        sections = []
        for provider in self.options_providers:
            for section, options in provider.options_by_section():
                if section is None:
                    section = provider.name
                if section in skipsections:
                    continue
                options = [(n, d, v) for (n, d, v) in options
                           if d.get('type') is not None
                           and not d.get('deprecated')]
                if not options:
                    continue
                if section not in sections:
                    sections.append(section)
                alloptions = options_by_section.setdefault(section, [])
                alloptions += options
        stream = stream or sys.stdout
        printed = False
        for section in sections:
            if printed:
                print('\n', file=stream)
            utils.format_section(stream, section.upper(),
                                 sorted(options_by_section[section]))
            printed = True

    def generate_manpage(self, pkginfo, section=1, stream=None):
        with _patch_optparse():
            _generate_manpage(self.cmdline_parser, pkginfo,
                              section, stream=stream or sys.stdout,
                              level=self._maxlevel)

    def load_provider_defaults(self):
        """initialize configuration using default values"""
        for provider in self.options_providers:
            provider.load_defaults()

    def read_config_file(self, config_file=None, verbose=None):
        """read the configuration file but do not load it (i.e. dispatching
        values to each options provider)
        """
        """
        helplevel = 1
        while helplevel <= self._maxlevel:
            opt = '-'.join(['long'] * helplevel) + '-help'
            if opt in self._all_options:
                break # already processed
            # pylint: disable=unused-argument
            def helpfunc(option, opt, val, p, level=helplevel):
                print(self.help(level))
                sys.exit(0)
            helpmsg = '%s verbose help.' % ' '.join(['more'] * helplevel)
            optdict = {'action': 'callback', 'callback': helpfunc,
                       'help': helpmsg}
            provider = self.options_providers[0]
            self.add_optik_option(provider, self.cmdline_parser, opt, optdict)
            provider.options += ((opt, optdict),)
            helplevel += 1
        """
        if config_file is None:
            config_file = self.config_file
        if config_file is not None:
            config_file = os.path.expanduser(config_file)
            if not os.path.exists(config_file):
                raise IOError("The config file {:s} doesn't exist!".format(config_file))

        use_config_file = config_file and os.path.exists(config_file)
        if use_config_file:
            self.cfgfile_parser.parse(config_file, Configuration())

        if not verbose:
            return

        if use_config_file:
            msg = 'Using config file {0}'.format(os.path.abspath(config_file))
        else:
            msg = 'No config file found, using default configuration'
        print(msg, file=sys.stderr)

    def load_config_file(self):
        """dispatch values previously read from a configuration file to each
        options provider)
        """
        for section in self.cfgfile_parser._parser.sections():
            for option, value in self.cfgfile_parser._parser.items(section):
                try:
                    self.global_set_option(option, value)
                except (KeyError, optparse.OptionError):
                    # TODO handle here undeclared options appearing in the config file
                    continue

    def load_configuration(self, **kwargs):
        """override configuration according to given parameters"""
        return self.load_configuration_from_config(kwargs)

    def load_configuration_from_config(self, config):
        for opt, opt_value in config.items():
            opt = opt.replace('_', '-')
            provider = self._all_options[opt]
            provider.set_option(opt, opt_value)

    def load_command_line_configuration(self, args=None):
        """Override configuration according to command line parameters

        return additional arguments
        """
        if args is None:
            args = sys.argv[1:]
        else:
            args = list(args)
        for provider in self._nocallback_options:
            self.cmdline_parser.parse(args, provider.config)
        config = Configuration()
        self.cmdline_parser.parse(args, config)
        return config.module_or_package

    def add_help_section(self, title, description, level=0):
        """add a dummy option section for help purpose """
        group = self.cmdline_parser._parser.add_argument_group(
            title.capitalize(), description, level=level
        )
        self._maxlevel = max(self._maxlevel, level)

    def help(self, level=0):
        """return the usage string for available options """
        return self.cmdline_parser._parser.format_help(level)


class OptionsProviderMixIn(object):
    """Mixin to provide options to an OptionsManager"""

    # those attributes should be overridden
    priority = -1
    name = 'default'
    options = ()
    level = 0

    def __init__(self):
        self.config = Configuration()
        self.load_defaults()

    def load_defaults(self):
        """initialize the provider using default values"""
        for opt, optdict in self.options:
            action = optdict.get('action')
            if action != 'callback':
                # callback action have no default
                if optdict is None:
                    optdict = self.get_option_def(opt)
                default = optdict.get('default')
                self.set_option(opt, default, action, optdict)

    def option_attrname(self, opt, optdict=None):
        """get the config attribute corresponding to opt"""
        if optdict is None:
            optdict = self.get_option_def(opt)
        return optdict.get('dest', opt.replace('-', '_'))

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
            action = optdict.get('action', 'store')
        if action == 'store':
            setattr(self.config, self.option_attrname(optname, optdict), value)
        elif action in ('store_true', 'count'):
            setattr(self.config, self.option_attrname(optname, optdict), 0)
        elif action == 'store_false':
            setattr(self.config, self.option_attrname(optname, optdict), 1)
        elif action == 'append':
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
        elif action == 'callback':
            optdict['callback'](None, optname, value, None)
        else:
            raise UnsupportedAction(action)

    def get_option_def(self, opt):
        """return the dictionary defining an option given its name"""
        assert self.options
        for option in self.options:
            if option[0] == opt:
                return option[1]
        raise optparse.OptionError('no such option %s in section %r'
                                   % (opt, self.name), opt)

    def options_by_section(self):
        """return an iterator on options grouped by section

        (section, [list of (optname, optdict, optvalue)])
        """
        sections = {}
        for optname, optdict in self.options:
            sections.setdefault(optdict.get('group'), []).append(
                (optname, optdict, self.option_value(optname)))
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
            kwargs.setdefault('usage', '')
        kwargs.setdefault('quiet', 1)
        OptionsManagerMixIn.__init__(self, *args, **kwargs)
        OptionsProviderMixIn.__init__(self)
        if not getattr(self, 'option_groups', None):
            self.option_groups = []
            for _, optdict in self.options:
                try:
                    gdef = (optdict['group'].upper(), '')
                except KeyError:
                    continue
                if gdef not in self.option_groups:
                    self.option_groups.append(gdef)
        self.register_options_provider(self, own_group=False)


def _generate_manpage(optparser, pkginfo, section=1,
                      stream=sys.stdout, level=0):
    formatter = _ManHelpFormatter()
    formatter.output_level = level
    formatter.parser = optparser
    print(formatter.format_head(optparser, pkginfo, section), file=stream)
    print(optparser.format_option_help(formatter), file=stream)
    print(formatter.format_tail(pkginfo), file=stream)


OptionDefinition = collections.namedtuple(
    'OptionDefinition', ['name', 'definition']
)


class Configuration(object):
    def __init__(self):
        self._option_definitions = {}

    def add_option(self, option_definition):
        name, definition = option_definition
        if name in self._option_definitions:
            # TODO: Raise something more sensible
            raise Exception('Option "{0}" already exists.')
        self._option_definitions[name] = definition


    def add_options(self, option_definitions):
        for option_definition in option_definitions:
            self.add_option(option_definition)

    def set_option(self, option, value):
        setattr(self, option, value)

    def copy(self):
        result = self.__class__()
        result.add_options(six.iteritems(self._option_definitions))

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
            value = getattr(other, option)
            setattr(result, option, value)

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
        for cfg_dir in walk_up(path):
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
            for parent_config in reversed(parent_configs):
                config += parent_config

            self._cache['path'] = config

        return config

    def __getitem__(self, path):
        return self.get_config_for(path)

    def __setitem__(self, path, config):
        return self.add_config_for(path, config)


@six.add_metaclass(abc.ABCMeta)
class ConfigParser(object):
    def __init__(self):
        self._option_definitions = {}
        self._option_groups = set()

    def add_option_definitions(self, option_definitions):
        self._option_definitions.update(option_definitions)

        for _, definition_dict in option_definitions:
            try:
                group = optdict['group'].upper()
            except KeyError:
                continue
            else:
                self._option_groups.add(group)

    def add_option_definition(self, option_definition):
        self.add_option_definitions([option_definition])

    @abc.abstractmethod
    def parse(self, to_parse, config):
        """Parse the given object into the config object.
        Args:
            to_parse (object): The object to parse.
            config (Configuration): The config object to parse into.
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
        option_groups = collections.defaultdict(list)

        for option, definition in option_definitions:
            group, args, kwargs = self._convert_definition(option, definition)
            option_groups[group].append(args, kwargs)

        for args, kwargs in option_groups['DEFAULT']:
            self._parser.add_argument(*args, **kwargs)

        del option_groups['DEFAULT']

        for group, arguments in six.iteritems(option_groups):
            self._option_groups.add(group)
            self._parser.add_argument_group(group.title())
            for args, kwargs in arguments:
                self._parser.add_argument(*args, **kwargs)

    @staticmethod
    def _convert_definition(option, definition):
        """Convert an option definition to a set of arguments for add_argument.

        Args:
            option (str): The name of the option
            definition (dict): The argument definition to convert.

        Returns:
            tuple(str, list, dict): A tuple of the group to add the argument to,
            plus the args and kwargs for :func:`ArgumentParser.add_argument`.

        Raises:
            Exception: When the definition is invalid.
        """
        args = []

        if 'short' in definition:
            args.append('-{0}'.format(definition['short']))

        args.append('--{0}'.format(option))

        copy_keys = ('action', 'default', 'dest', 'help', 'metavar', 'level')
        kwargs = {k: definition[k] for k in copy_keys if k in definition}

        if 'type' in definition:
            if definition['type'] in VALIDATORS:
                kwargs['type'] = VALIDATORS[definition['type']]
            elif definition['type'] in ('choice', 'multiple_choice'):
                if 'choices' not in definition:
                    msg = 'No choice list given for option "{0}" of type "choice".'
                    msg = msg.format(option)
                    # TODO: Raise something more sensible
                    raise Exception(msg)

                if definition['type'] == 'multiple_choice':
                    kwargs['type'] = VALIDATORS['csv']

                kwargs['choices'] = definition['choices']
            else:
                msg = 'Unsupported type "{0}"'.format(definition['type'])
                # TODO: Raise something more sensible
                raise Exception(msg)

        if definition.get('hide'):
            kwargs['help'] = argparse.SUPPRESS

        group = definition.get('group', 'DEFAULT').upper()
        return group, args, kwargs

    def parse(self, argv, config):
        """Parse the command line arguments into the given config object.
        Args:
            argv (list(str)): The command line arguments to parse.
            config (Configuration): The config object to parse
                the command line into.
        """
        self._parser.parse_args(argv, config)

    def preprocess(self, argv, *options):
        """Do some guess work to get a value for the specified option.
        Args:
            argv (list(str)): The command line arguments to parse.
            *options (str): The names of the options to look for.
        Returns:
            Configuration: A config with the processed options.
        """
        config = Config()
        config.add_options(self._option_definitions)

        args = self._parser.parse_known_args(argv)[0]
        for option in options:
            config.set_option(option, getattr(args, option, None))

        return config


@six.add_metaclass(abc.ABCMeta)
class FileParser(ConfigParser):
    @abc.abstractmethod
    def parse(self, file_path, config):
        pass


class IniFileParser(FileParser):
    """Parses a config files into config objects."""

    def __init__(self):
        super(IniFileParser, self).__init__()
        self._parser = configparser.ConfigParser(
            inline_comment_prefixes=('#', ';'),
        )

    def add_option_definitions(self, option_definitions):
        for option, definition in option_definitions:
            group, default = self._convert_definition(option, definition)

            try:
                self._parser.add_section(group)
            except configparser.DuplicateSectionError:
                pass
            else:
                self._option_groups.add(group)

            # TODO: Do we need to do this?
            self._parser['DEFAULT'].update(default)

    @staticmethod
    def _convert_definition(option, definition):
        """Convert an option definition to a set of arguments for the parser.

        Args:
            option (str): The name of the option.
            definition (dict): The argument definition to convert.
        """
        default = {option: definition.get('default')}

        group = definition.get('group', 'DEFAULT').upper()
        return group, default

    def parse(self, file_path, config):
        self._parser.read(file_path)

        for section in self._parser.sections():
            # Normalise the section titles
            if not section.isupper():
                new_section = section.upper()
                for option, value in self._parser.items(section):
                    self._parser.set(new_section, option, value)
                self._parser.remove_section(section)
                section = section.upper()

            for option, value in self._parser.items(section):
                config.set_option(option, value)


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


class LongHelpArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, formatter_class=LongHelpFormatter, **kwargs):
        self._max_level = 0
        super(LongHelpArgumentParser, self).__init__(
            *args, formatter_class=formatter_class, **kwargs
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

        Returns:
            argparse.Action: The created action.
        """
        level = kwargs.pop('level', 0)
        action = super(LongHelpArgumentParser, self).add_argument(*args, **kwargs)
        action.level = level
        return action

    def add_argument_group(self, *args, level=0, **kwargs):
        group = super(LongHelpArgumentParser, self).add_argument_group(
            *args, **kwargs
        )
        group.level = level
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
