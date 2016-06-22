# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""some various utilities and helper classes, most of them used in the
main pylint class
"""
from __future__ import print_function

import collections
import os
from os.path import dirname, basename, splitext, exists, isdir, join, normpath
import re
import sys
import tokenize
import textwrap

import six

from astroid import modutils

from pylint.reporters.ureports.nodes import Section
from pylint._internal.message import MessageDefinition


_MSG_ORDER = 'EWRCIF'
# Allow stopping after the first semicolon encountered,
# so that an option can be continued with the reasons
# why it is active or disabled.
OPTION_RGX = re.compile(r'\s*#.*\bpylint:\s*([^;]+);{0,1}')


class EmptyReport(Exception):
    """raised when a report is empty and so should not be displayed"""


def _decoding_readline(stream, encoding):
    return lambda: stream.readline().decode(encoding, 'replace')


def tokenize_module(module):
    with module.stream() as stream:
        readline = stream.readline
        if sys.version_info < (3, 0):
            if module.file_encoding is not None:
                readline = _decoding_readline(stream, module.file_encoding)

            return list(tokenize.generate_tokens(readline))
        return list(tokenize.tokenize(readline))


class ReportsHandlerMixIn(object):
    """a mix-in class containing all the reports and stats manipulation
    related methods for the main lint class
    """
    def __init__(self):
        self._reports = collections.defaultdict(list)
        self._reports_state = {}

    def report_order(self):
        """ Return a list of reports, sorted in the order
        in which they must be called.
        """
        return list(self._reports)

    def register_report(self, reportid, r_title, r_cb, checker):
        """register a report

        reportid is the unique identifier for the report
        r_title the report's title
        r_cb the method to call to make the report
        checker is the checker defining the report
        """
        reportid = reportid.upper()
        self._reports[checker].append((reportid, r_title, r_cb))

    def enable_report(self, reportid):
        """disable the report of the given id"""
        reportid = reportid.upper()
        self._reports_state[reportid] = True

    def disable_report(self, reportid):
        """disable the report of the given id"""
        reportid = reportid.upper()
        self._reports_state[reportid] = False

    def report_is_enabled(self, reportid):
        """return true if the report associated to the given identifier is
        enabled
        """
        return self._reports_state.get(reportid, True)

    def make_reports(self, stats, old_stats):
        """render registered reports"""
        sect = Section('Report',
                       '%s statements analysed.'% (self.stats['statement']))
        for checker in self.report_order():
            for reportid, r_title, r_cb in self._reports[checker]:
                if not self.report_is_enabled(reportid):
                    continue
                report_sect = Section(r_title)
                try:
                    r_cb(report_sect, stats, old_stats)
                except EmptyReport:
                    continue
                report_sect.report_id = reportid
                sect.append(report_sect)
        return sect

    def add_stats(self, **kwargs):
        """add some stats entries to the statistic dictionary
        raise an AssertionError if there is a key conflict
        """
        for key, value in six.iteritems(kwargs):
            if key[-1] == '_':
                key = key[:-1]
            assert key not in self.stats
            self.stats[key] = value
        return self.stats

def _basename_in_blacklist_re(base_name, black_list_re):
    """Determines if the basename is matched in a regex blacklist

    :param base_name: The basename of the file
    :param black_list_re: A collection of regex patterns to match against. Successful matches are
                          blacklisted.
    :returns: `True` if the basename is blacklisted, `False` otherwise.

    """

    for file_pattern in black_list_re:
        if file_pattern.match(base_name):
            return True
    return False

def _modpath_from_file(filename, is_namespace):
    def _is_package_cb(path, parts):
        return modutils.check_modpath_has_init(path, parts) or is_namespace

    return modutils.modpath_from_file_with_callback(filename, is_package_cb=_is_package_cb)


def expand_modules(files_or_modules, black_list, black_list_re):
    """take a list of files/modules/packages and return the list of tuple
    (file, module name) which have to be actually checked
    """
    result = []
    errors = []
    for something in files_or_modules:
        if exists(something):
            # this is a file or a directory
            try:
                modname = '.'.join(modutils.modpath_from_file(something))
            except ImportError:
                modname = splitext(basename(something))[0]
            if isdir(something):
                filepath = join(something, '__init__.py')
            else:
                filepath = something
        else:
            # suppose it's a module or package
            modname = something
            try:
                filepath = modutils.file_from_modpath(modname.split('.'))
                if filepath is None:
                    continue
            except (ImportError, SyntaxError) as ex:
                # FIXME p3k : the SyntaxError is a Python bug and should be
                # removed as soon as possible http://bugs.python.org/issue10588
                errors.append({'key': 'fatal', 'mod': modname, 'ex': ex})
                continue

        filepath = normpath(filepath)
        modparts = (modname or something).split('.')

        try:
            spec = modutils.file_info_from_modpath(modparts, path=sys.path)
        except ImportError:
            # Might not be acceptable, don't crash.
            is_namespace = False
            is_directory = isdir(something)
        else:
            is_namespace = spec.type == modutils.ModuleType.PY_NAMESPACE
            is_directory = spec.type == modutils.ModuleType.PKG_DIRECTORY

        if not is_namespace:
            result.append({'path': filepath, 'name': modname, 'isarg': True,
                           'basepath': filepath, 'basename': modname})

        has_init = (not (modname.endswith('.__init__') or modname == '__init__')
                    and '__init__.py' in filepath)

        if has_init or is_namespace or is_directory:
            for subfilepath in modutils.get_module_files(dirname(filepath), black_list,
                                                         list_all=is_namespace):
                if filepath == subfilepath:
                    continue
                if _basename_in_blacklist_re(basename(subfilepath), black_list_re):
                    continue

                modpath = _modpath_from_file(subfilepath, is_namespace)
                submodname = '.'.join(modpath)
                result.append({'path': subfilepath, 'name': submodname,
                               'isarg': False,
                               'basepath': filepath, 'basename': modname})
    return result, errors



PY_EXTS = ('.py', '.pyc', '.pyo', '.pyw', '.so', '.dll')

def register_plugins(linter, directory):
    """load all module and package in the given directory, looking for a
    'register' function in each one, used to register pylint checkers
    """
    imported = {}
    for filename in os.listdir(directory):
        base, extension = splitext(filename)
        if base in imported or base == '__pycache__':
            continue
        if extension in PY_EXTS and base != '__init__' or (
                not extension and isdir(join(directory, base))):
            try:
                module = modutils.load_module_from_file(join(directory, filename))
            except ValueError:
                # empty module name (usually emacs auto-save files)
                continue
            except ImportError as exc:
                print("Problem importing module %s: %s" % (filename, exc),
                      file=sys.stderr)
            else:
                if hasattr(module, 'register'):
                    module.register(linter)
                    imported[base] = 1

def get_global_option(checker, option, default=None):
    """ Retrieve an option defined by the given *checker* or
    by all known option providers.

    It will look in the list of all options providers
    until the given *option* will be found.
    If the option wasn't found, the *default* value will be returned.
    """
    # First, try in the given checker's config.
    # After that, look in the options providers.

    try:
        return getattr(checker.config, option.replace("-", "_"))
    except AttributeError:
        pass
    for provider in checker.linter.options_providers:
        for options in provider.options:
            if options[0] == option:
                return getattr(provider.config, option.replace("-", "_"))
    return default


def deprecated_option(shortname=None, opt_type=None, help_msg=None):
    def _warn_deprecated(option, optname, *args): # pylint: disable=unused-argument
        msg = ("Warning: option %s is obsolete and "
               "it is slated for removal in Pylint 1.6.\n")
        sys.stderr.write(msg % (optname,))

    option = {
        'help': help_msg,
        'hide': True,
        'type': opt_type,
        'action': 'callback',
        'callback': _warn_deprecated,
        'deprecated': True
    }
    if shortname:
        option['shortname'] = shortname
    return option


def _splitstrip(string, sep=','):
    """return a list of stripped string by splitting the string given as
    argument on `sep` (',' by default). Empty string are discarded.

    >>> _splitstrip('a, b, c   ,  4,,')
    ['a', 'b', 'c', '4']
    >>> _splitstrip('a')
    ['a']
    >>>

    :type string: str or unicode
    :param string: a csv line

    :type sep: str or unicode
    :param sep: field separator, default to the comma (',')

    :rtype: str or unicode
    :return: the unquoted string (or the input string if it wasn't quoted)
    """
    return [word.strip() for word in string.split(sep) if word.strip()]


def _unquote(string):
    """remove optional quotes (simple or double) from the string

    :type string: str or unicode
    :param string: an optionally quoted string

    :rtype: str or unicode
    :return: the unquoted string (or the input string if it wasn't quoted)
    """
    if not string:
        return string
    if string[0] in '"\'':
        string = string[1:]
    if string[-1] in '"\'':
        string = string[:-1]
    return string


def _normalize_text(text, line_len=80, indent=''):
    """Wrap the text on the given line length."""
    return '\n'.join(textwrap.wrap(text, width=line_len, initial_indent=indent,
                                   subsequent_indent=indent))


def _check_csv(value):
    if isinstance(value, (list, tuple)):
        return value
    return _splitstrip(value)


if six.PY2:
    def _encode(string, encoding):
        # pylint: disable=undefined-variable
        if isinstance(string, unicode):
            return string.encode(encoding)
        return str(string)
else:
    def _encode(string, _):
        return str(string)

def _get_encoding(encoding, stream):
    encoding = encoding or getattr(stream, 'encoding', None)
    if not encoding:
        import locale
        encoding = locale.getpreferredencoding()
    return encoding


def _comment(string):
    """return string as a comment"""
    lines = [line.strip() for line in string.splitlines()]
    return '# ' + ('%s# ' % os.linesep).join(lines)


def _format_option_value(optdict, value):
    """return the user input's value from a 'compiled' value"""
    if isinstance(value, (list, tuple)):
        value = ','.join(value)
    elif isinstance(value, dict):
        value = ','.join('%s:%s' % (k, v) for k, v in value.items())
    elif hasattr(value, 'match'): # optdict.get('type') == 'regexp'
        # compiled regexp
        value = value.pattern
    elif optdict.get('type') == 'yn':
        value = value and 'yes' or 'no'
    elif isinstance(value, six.string_types) and value.isspace():
        value = "'%s'" % value
    return value


def _ini_format_section(stream, section, options, encoding=None, doc=None):
    """format an options section using the INI format"""
    encoding = _get_encoding(encoding, stream)
    if doc:
        print(_encode(_comment(doc), encoding), file=stream)
    print('[%s]' % section, file=stream)
    _ini_format(stream, options, encoding)


def _ini_format(stream, options, encoding):
    """format options using the INI format"""
    for optname, optdict, value in options:
        value = _format_option_value(optdict, value)
        help = optdict.get('help')
        if help:
            help = _normalize_text(help, line_len=79, indent='# ')
            print(file=stream)
            print(_encode(help, encoding), file=stream)
        else:
            print(file=stream)
        if value is None:
            print('#%s=' % optname, file=stream)
        else:
            value = _encode(value, encoding).strip()
            print('%s=%s' % (optname, value), file=stream)

format_section = _ini_format_section


def _rest_format_section(stream, section, options, encoding=None, doc=None):
    """format an options section using as ReST formatted output"""
    encoding = _get_encoding(encoding, stream)
    if section:
        print('%s\n%s' % (section, "'"*len(section)), file=stream)
    if doc:
        print(_encode(_normalize_text(doc, line_len=79, indent=''), encoding), file=stream)
        print(file=stream)
    for optname, optdict, value in options:
        help = optdict.get('help')
        print(':%s:' % optname, file=stream)
        if help:
            help = _normalize_text(help, line_len=79, indent='  ')
            print(_encode(help, encoding), file=stream)
        if value:
            value = _encode(_format_option_value(optdict, value), encoding)
            print(file=stream)
            print('  Default: ``%s``' % value.replace("`` ", "```` ``"), file=stream)


def print_full_documentation(linter):
    """output a full documentation in ReST format"""
    print("Pylint global options and switches")
    print("----------------------------------")
    print("")
    print("Pylint provides global options and switches.")
    print("")

    by_checker = {}
    for checker in linter.get_checkers():
        if checker.name == 'master':
            if checker.options:
                for section, options in checker.options_by_section():
                    if section is None:
                        title = 'General options'
                    else:
                        title = '%s options' % section.capitalize()
                    print(title)
                    print('~' * len(title))
                    _rest_format_section(sys.stdout, None, options)
                    print("")
        else:
            try:
                by_checker[checker.name][0] += checker.options_and_values()
                by_checker[checker.name][1].update(checker.msgs)
                by_checker[checker.name][2] += checker.reports
            except KeyError:
                by_checker[checker.name] = [list(checker.options_and_values()),
                                            dict(checker.msgs),
                                            list(checker.reports)]

    print("Pylint checkers' options and switches")
    print("-------------------------------------")
    print("")
    print("Pylint checkers can provide three set of features:")
    print("")
    print("* options that control their execution,")
    print("* messages that they can raise,")
    print("* reports that they can generate.")
    print("")
    print("Below is a list of all checkers and their features.")
    print("")

    for checker, (options, msgs, reports) in six.iteritems(by_checker):
        title = '%s checker' % (checker.replace("_", " ").title())
        print(title)
        print('~' * len(title))
        print("")
        print("Verbatim name of the checker is ``%s``." % checker)
        print("")
        if options:
            title = 'Options'
            print(title)
            print('^' * len(title))
            _rest_format_section(sys.stdout, None, options)
            print("")
        if msgs:
            title = 'Messages'
            print(title)
            print('~' * len(title))
            for msgid, msg in sorted(six.iteritems(msgs),
                                     key=lambda kv: (_MSG_ORDER.index(kv[0][0]), kv[1])):
                msg = MessageDefinition.from_message_def(checker, msgid, msg)
                print(msg.format_help(checkerref=False))
            print("")
        if reports:
            title = 'Reports'
            print(title)
            print('~' * len(title))
            for report in reports:
                print(':%s: %s' % report[:2])
            print("")
        print("")
