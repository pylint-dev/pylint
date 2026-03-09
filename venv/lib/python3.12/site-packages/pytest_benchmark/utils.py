"""
..
  PYTEST_DONT_REWRITE
"""

import argparse
import json
import netrc
import os
import platform
import re
import subprocess
import sys
from datetime import datetime
from datetime import timezone
from decimal import Decimal
from functools import partial
from os.path import split
from pathlib import Path
from subprocess import CalledProcessError
from subprocess import check_output
from urllib.parse import parse_qs
from urllib.parse import urlparse

TIME_UNITS = {'': 'Seconds', 'm': 'Milliseconds (ms)', 'u': 'Microseconds (us)', 'n': 'Nanoseconds (ns)'}
ALLOWED_COLUMNS = ['min', 'max', 'mean', 'stddev', 'median', 'iqr', 'ops', 'outliers', 'rounds', 'iterations']


class SecondsDecimal(Decimal):
    def __float__(self):
        return float(super().__str__())

    def __str__(self):
        return f'{format_time(float(super().__str__()))}s'

    @property
    def as_string(self):
        return super().__str__()


class NameWrapper:
    def __init__(self, target):
        self.target = target

    def __str__(self):
        name = self.target.__module__ + '.' if hasattr(self.target, '__module__') else ''
        name += self.target.__name__ if hasattr(self.target, '__name__') else repr(self.target)
        return name

    def __repr__(self):
        return f'NameWrapper({self.target!r})'


def get_tag(project_name=None):
    info = get_commit_info(project_name)
    parts = [info['id'], get_current_time()]
    if info['dirty']:
        parts.append('uncommited-changes')
    return '_'.join(parts)


def get_machine_id():
    return '{}-{}-{}-{}'.format(
        platform.system(),
        platform.python_implementation(),
        '.'.join(platform.python_version_tuple()[:2]),
        platform.architecture()[0],
    )


class Fallback:
    def __init__(self, fallback, exceptions):
        self.fallback = fallback
        self.functions = []
        self.exceptions = exceptions

    def __call__(self, *args, **kwargs):
        for func in self.functions:
            try:
                value = func(*args, **kwargs)
            except self.exceptions:
                continue
            else:
                if value:
                    return value
        else:
            return self.fallback(*args, **kwargs)

    def register(self, other):
        self.functions.append(other)
        return self


@partial(Fallback, exceptions=(IndexError, CalledProcessError, OSError))
def get_project_name():
    return Path.cwd().name


@get_project_name.register
def get_project_name_git():
    is_git = check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.STDOUT)
    if is_git:
        project_address = check_output(['git', 'config', '--local', 'remote.origin.url'])
        if isinstance(project_address, bytes):
            project_address = project_address.decode()
        project_name = [i for i in re.split(r'[/:\s\\]|\.git', project_address) if i][-1]
        return project_name.strip()


@get_project_name.register
def get_project_name_hg():
    with open(os.devnull, 'w') as devnull:
        project_address = check_output(['hg', 'path', 'default'], stderr=devnull)
    project_address = project_address.decode()
    project_name = project_address.split('/')[-1]
    return project_name.strip()


def in_any_parent(name, path=None):
    prev = None
    if not path:
        path = Path.cwd()
    while path and prev != path and not path.joinpath(name).exists():
        prev = path
        path = path.parent
    return path.joinpath(name).exists()


def subprocess_output(cmd):
    return check_output(cmd.split(), stderr=subprocess.STDOUT, universal_newlines=True).strip()


def get_commit_info(project_name=None):
    dirty = False
    commit = 'unversioned'
    commit_time = None
    author_time = None
    project_name = project_name or get_project_name()
    branch = '(unknown)'
    try:
        if in_any_parent('.git'):
            desc = subprocess_output('git describe --dirty --always --long --abbrev=40')
            desc = desc.split('-')
            if desc[-1].strip() == 'dirty':
                dirty = True
                desc.pop()
            commit = desc[-1].strip('g')
            commit_time = subprocess_output('git show -s --pretty=format:"%cI"').strip('"')
            author_time = subprocess_output('git show -s --pretty=format:"%aI"').strip('"')
            branch = subprocess_output('git rev-parse --abbrev-ref HEAD')
            if branch == 'HEAD':
                branch = '(detached head)'
        elif in_any_parent('.hg'):
            desc = subprocess_output('hg id --id --debug')
            if desc[-1] == '+':
                dirty = True
            commit = desc.strip('+')
            commit_time = subprocess_output('hg tip --template "{date|rfc3339date}"').strip('"')
            branch = subprocess_output('hg branch')
        return {
            'id': commit,
            'time': commit_time,
            'author_time': author_time,
            'dirty': dirty,
            'project': project_name,
            'branch': branch,
        }
    except Exception as exc:
        return {
            'id': 'unknown',
            'time': None,
            'author_time': None,
            'dirty': dirty,
            'error': f'CalledProcessError({exc.returncode}, {exc.output!r})' if isinstance(exc, CalledProcessError) else repr(exc),
            'project': project_name,
            'branch': branch,
        }


def get_current_time():
    return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')


def first_or_value(obj, value):
    if obj:
        (value,) = obj

    return value


def short_filename(path, machine_id=None):
    parts = []
    try:
        last = len(path.parts) - 1
    except AttributeError:
        return str(path)
    for pos, part in enumerate(path.parts):
        if not pos and part == machine_id:
            continue
        if pos == last:
            part = part.rsplit('.', 1)[0]
            # if len(part) > 16:
            #     part = "%.13s..." % part
        parts.append(part)
    return '/'.join(parts)


def load_timer(string):
    if '.' not in string:
        raise argparse.ArgumentTypeError("Value for --benchmark-timer must be in dotted form. Eg: 'module.attr'.")
    mod, attr = string.rsplit('.', 1)
    if mod == 'pep418':
        import time  # noqa: PLC0415

        return NameWrapper(getattr(time, attr))
    else:
        __import__(mod)
        mod = sys.modules[mod]
        return NameWrapper(getattr(mod, attr))


class RegressionCheck:
    def __init__(self, field, threshold):
        self.field = field
        self.threshold = threshold

    def fails(self, current, compared):
        val = self.compute(current, compared)
        if val > self.threshold:
            return f'Field {self.field!r} has failed {self.__class__.__name__}: {val:.9f} > {self.threshold:.9f}'


class PercentageRegressionCheck(RegressionCheck):
    def compute(self, current, compared):
        val = compared[self.field]
        if not val:
            return float('inf')
        return current[self.field] / val * 100 - 100


class DifferenceRegressionCheck(RegressionCheck):
    def compute(self, current, compared):
        return current[self.field] - compared[self.field]


def parse_compare_fail(
    string,
    rex=re.compile(
        r'^(?P<field>min|max|mean|median|stddev|iqr):' r'((?P<percentage>[0-9]+)%|(?P<difference>[0-9]*\.?[0-9]+([eE][-+]?[' r'0-9]+)?))$'
    ),
):
    m = rex.match(string)
    if m:
        g = m.groupdict()
        if g['percentage']:
            return PercentageRegressionCheck(g['field'], int(g['percentage']))
        elif g['difference']:
            return DifferenceRegressionCheck(g['field'], float(g['difference']))

    raise argparse.ArgumentTypeError(f'Could not parse value: {string!r}.')


def parse_cprofile_loops(string):
    if string == 'auto':
        return None
    else:
        try:
            value = int(string)
        except ValueError:
            raise argparse.ArgumentTypeError(f'Could not parse value: {string!r}. Expected an integer or `auto`.') from None
        if value < 1:
            raise argparse.ArgumentTypeError(f'Invalid value: {string!r}. Must be greater than 0.') from None
        return value


def parse_warmup(string):
    string = string.lower().strip()
    if string == 'auto':
        return platform.python_implementation() == 'PyPy'
    elif string in ['off', 'false', 'no']:
        return False
    elif string in ['on', 'true', 'yes', '']:
        return True
    else:
        raise argparse.ArgumentTypeError(f'Could not parse value: {string!r}.')


def name_formatter_short(bench):
    name = bench['name']
    if bench['source']:
        name = '{} ({:.4})'.format(name, split(bench['source'])[-1])
    if name.startswith('test_'):
        name = name[5:]
    return name


def name_formatter_normal(bench):
    name = bench['name']
    if bench['source']:
        parts = bench['source'].split('/')
        parts[-1] = parts[-1][:12]
        name = '{} ({})'.format(name, '/'.join(parts))
    return name


def name_formatter_long(bench):
    if bench['source']:
        return '{fullname} ({source})'.format(**bench)
    else:
        return bench['fullname']


def name_formatter_trial(bench):
    if bench['source']:
        return '{:.4}'.format(split(bench['source'])[-1])
    else:
        return '????'


NAME_FORMATTERS = {
    'short': name_formatter_short,
    'normal': name_formatter_normal,
    'long': name_formatter_long,
    'trial': name_formatter_trial,
}


def parse_name_format(string):
    string = string.lower().strip()
    if string in NAME_FORMATTERS:
        return string
    else:
        raise argparse.ArgumentTypeError(f'Could not parse value: {string!r}.')


def parse_timer(string):
    return str(load_timer(string))


def parse_sort(string):
    string = string.lower().strip()
    if string not in ('min', 'max', 'mean', 'stddev', 'name', 'fullname'):
        raise argparse.ArgumentTypeError(
            f'Unacceptable value: {string!r}. '
            "Value for --benchmark-sort must be one of: 'min', 'max', 'mean', "
            "'stddev', 'name', 'fullname'."
        )
    return string


def parse_columns(string):
    columns = [str.strip(s) for s in string.lower().split(',')]
    invalid = set(columns) - set(ALLOWED_COLUMNS)
    if invalid:
        # there are extra items in columns!
        msg = 'Invalid column name(s): {}. '.format(', '.join(invalid))
        msg += 'The only valid column names are: {}'.format(', '.join(ALLOWED_COLUMNS))
        raise argparse.ArgumentTypeError(msg)
    return columns


def parse_rounds(string):
    try:
        value = int(string)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(exc) from None
    else:
        if value < 1:
            raise argparse.ArgumentTypeError('Value for --benchmark-rounds must be at least 1.')
        return value


def parse_seconds(string):
    try:
        return SecondsDecimal(string).as_string
    except Exception as exc:
        raise argparse.ArgumentTypeError(f'Invalid decimal value {string!r}: {exc!r}') from None


def parse_save(string):
    if not string:
        raise argparse.ArgumentTypeError("Can't be empty.")
    illegal = ''.join(c for c in r'\/:*?<>|' if c in string)
    if illegal:
        raise argparse.ArgumentTypeError(f'Must not contain any of these characters: /:*?<>|\\ (it has {illegal!r})')
    return string


def _parse_hosts(storage_url, netrc_file):
    # load creds from netrc file
    path = Path(netrc_file).expanduser()
    creds = None
    if netrc_file and path.is_file():
        creds = netrc.netrc(path)

    # add creds to urls
    urls = []
    for netloc in storage_url.netloc.split(','):
        auth = ''
        if creds and '@' not in netloc:
            host = netloc.split(':').pop(0)
            res = creds.authenticators(host)
            if res:
                user, _, secret = res
                auth = f'{user}:{secret}@'
        url = f'{storage_url.scheme}://{auth}{netloc}'
        urls.append(url)
    return urls


def parse_elasticsearch_storage(string, default_index='benchmark', default_doctype='benchmark', netrc_file=''):
    storage_url = urlparse(string)
    hosts = _parse_hosts(storage_url, netrc_file)
    index = default_index
    doctype = default_doctype
    if storage_url.path and storage_url.path != '/':
        splitted = storage_url.path.strip('/').split('/')
        index = splitted[0]
        if len(splitted) >= 2:
            doctype = splitted[1]
    query = parse_qs(storage_url.query)
    try:
        project_name = query['project_name'][0]
    except KeyError:
        project_name = get_project_name()
    return hosts, index, doctype, project_name


def load_storage(storage, **kwargs):
    if '://' not in storage:
        storage = 'file://' + storage
    netrc_file = kwargs.pop('netrc')  # only used by elasticsearch storage
    if storage.startswith('file://'):
        from .storage.file import FileStorage  # noqa: PLC0415

        return FileStorage(storage[len('file://') :], **kwargs)
    elif storage.startswith('elasticsearch+'):
        from .storage.elasticsearch import ElasticsearchStorage  # noqa: PLC0415

        # TODO update benchmark_autosave
        args = parse_elasticsearch_storage(storage[len('elasticsearch+') :], netrc_file=netrc_file)
        return ElasticsearchStorage(*args, **kwargs)
    else:
        raise argparse.ArgumentTypeError('Storage must be in form of file://path or elasticsearch+http[s]://host1,host2/index/doctype')


def time_unit(value):
    if value < 1e-6:
        return 'n', 1e9
    elif value < 1e-3:
        return 'u', 1e6
    elif value < 1:
        return 'm', 1e3
    else:
        return '', 1.0


def operations_unit(value):
    if value > 1e6:
        return 'M', 1e-6
    if value > 1e3:
        return 'K', 1e-3
    return '', 1.0


def format_time(value):
    unit, adjustment = time_unit(value)
    return f'{value * adjustment:.2f}{unit:s}'


class cached_property:
    def __init__(self, func):
        self.__doc__ = func.__doc__
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def funcname(f):
    try:
        if isinstance(f, partial):
            return f.func.__name__
        else:
            return f.__name__
    except AttributeError:
        return str(f)


def clonefunc(f):
    """
    This used to be a slightly improved version of clonefunc from https://github.com/antocuni/pypytools/blob/master/pypytools/util.py

    It was supposed to make a copy of the function with a new code object so PyPy creates fresh JIT compilation for the given function,
    however, it has proven difficult to maintain and to even prove that it does what it supposed to do without breaking something.

    Now it simply does nothing - it returns the input function.
    """
    return f


class SafeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return f'UNSERIALIZABLE[{o!r}]'


def consistent_dumps(value):
    return json.dumps(value, sort_keys=True)


def safe_dumps(obj, **kwargs):
    return json.dumps(obj, cls=SafeJSONEncoder, **kwargs)


def report_progress(iterable, terminal_reporter, format_string, **kwargs):
    total = len(iterable)

    def progress_reporting_wrapper():
        for pos, item in enumerate(iterable):
            string = format_string.format(pos=pos + 1, total=total, value=item, **kwargs)
            terminal_reporter.rewrite(string, black=True, bold=True)
            yield string, item

    return progress_reporting_wrapper()


def report_noprogress(iterable, *args, **kwargs):
    for item in iterable:
        yield '', item


def report_online_progress(progress_reporter, tr, line):
    next(progress_reporter([line], tr, '{value}'))


def slugify(name):
    for c in r'\/:*?<>| ':
        name = name.replace(c, '_').replace('__', '_')
    return name


def get_cprofile_functions(stats):
    """
    Convert pstats structure to list of sorted dicts about each function.
    """
    result = []
    # this assumes that you run py.test from project root dir
    project_dir_parent = str(Path.cwd().parent)

    for function_info, run_info in stats.stats.items():
        file_path = function_info[0]
        if file_path.startswith(project_dir_parent):
            file_path = file_path[len(project_dir_parent) :].lstrip('/')
        function_name = f'{file_path}:{function_info[1]}({function_info[2]})'

        pcalls, ncalls, tottime, cumtime = run_info[:4]

        # if the function is recursive, write number of 'total calls/primitive calls'
        if pcalls == ncalls:
            calls = str(pcalls)
        else:
            calls = f'{ncalls}/{pcalls}'

        result.append(
            {
                'ncalls_recursion': calls,
                'ncalls': ncalls,
                'tottime': tottime,
                'tottime_per': tottime / pcalls if pcalls > 0 else 0,
                'cumtime': cumtime,
                'cumtime_per': cumtime / pcalls if pcalls > 0 else 0,
                'function_name': function_name,
            }
        )

    return result
