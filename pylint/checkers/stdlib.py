# -*- coding: utf-8 -*-
# Copyright (c) 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2013-2014 Google, Inc.
# Copyright (c) 2014-2017 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Cosmin Poieana <cmin@ropython.org>
# Copyright (c) 2014 Vlad Temian <vladtemian@gmail.com>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Cezar <celnazli@bitdefender.com>
# Copyright (c) 2015 Chris Rebert <code@rebertia.com>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 Jared Garst <cultofjared@gmail.com>
# Copyright (c) 2017 Martin <MartinBasti@users.noreply.github.com>
# Copyright (c) 2017 Christopher Zurcher <zurcher@users.noreply.github.com>
# Copyright (c) 2017 Łukasz Rogalski <rogalski.91@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Checkers for various standard library functions."""

import sys

import astroid
from astroid.bases import Instance
from astroid.node_classes import Const, Call
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker
from pylint.checkers import utils


OPEN_FILES = {'open', 'file'}
UNITTEST_CASE = 'unittest.case'
THREADING_THREAD = 'threading.Thread'
ENV_SETTERS = {'posix.putenv', 'os.putenv'}
ENV_GETTERS = {'os.getenv'}
ENV_FUNCTIONS = ENV_SETTERS.union(ENV_GETTERS)
COPY_COPY = 'copy.copy'
OS_ENVIRON = 'os._Environ'

if sys.version_info >= (3, 0):
    OPEN_MODULE = '_io'
else:
    OPEN_MODULE = '__builtin__'


def _check_mode_str(mode):
    # check type
    if not isinstance(mode, str):
        return False
    # check syntax
    modes = set(mode)
    _mode = "rwatb+Ux"
    creating = "x" in modes
    if modes - set(_mode) or len(mode) > len(modes):
        return False
    # check logic
    reading = "r" in modes
    writing = "w" in modes
    appending = "a" in modes
    text = "t" in modes
    binary = "b" in modes
    if "U" in modes:
        if writing or appending or creating:
            return False
        reading = True
    if text and binary:
        return False
    total = reading + writing + appending + creating
    if total > 1:
        return False
    if not (reading or writing or appending or creating):
        return False
    return True


class StdlibChecker(BaseChecker):
    __implements__ = (IAstroidChecker,)
    name = 'stdlib'

    msgs = {
        'W1501': ('"%s" is not a valid mode for open.',
                  'bad-open-mode',
                  'Python supports: r, w, a[, x] modes with b, +, '
                  'and U (only with r) options. '
                  'See http://docs.python.org/2/library/functions.html#open'),
        'W1502': ('Using datetime.time in a boolean context.',
                  'boolean-datetime',
                  'Using datetime.time in a boolean context can hide '
                  'subtle bugs when the time they represent matches '
                  'midnight UTC. This behaviour was fixed in Python 3.5. '
                  'See http://bugs.python.org/issue13936 for reference.',
                  {'maxversion': (3, 5)}),
        'W1503': ('Redundant use of %s with constant '
                  'value %r',
                  'redundant-unittest-assert',
                  'The first argument of assertTrue and assertFalse is '
                  'a condition. If a constant is passed as parameter, that '
                  'condition will be always true. In this case a warning '
                  'should be emitted.'),
        'W1505': ('Using deprecated method %s()',
                  'deprecated-method',
                  'The method is marked as deprecated and will be removed in '
                  'a future version of Python. Consider looking for an '
                  'alternative in the documentation.'),
        'W1506': ('threading.Thread needs the target function',
                  'bad-thread-instantiation',
                  'The warning is emitted when a threading.Thread class '
                  'is instantiated without the target function being passed. '
                  'By default, the first parameter is the group param, not the target param. '),
        'W1507': ('Using copy.copy(os.environ). Use os.environ.copy() '
                  'instead. ',
                  'shallow-copy-environ',
                  'os.environ is not a dict object but proxy object, so '
                  'shallow copy has still effects on original object. '
                  'See https://bugs.python.org/issue15373 for reference. '),
        'E1507': ('"%s" does not support %s type argument',
                  'invalid-envvar-value',
                  'Env manipulation functions support only string type arguments. '
                  'See https://docs.python.org/3/library/os.html#os.putenv. '),
        'W1508': ('"%s" default type is "%s". Expected str or None.',
                  'invalid-envvar-default',
                  'Env manipulation functions return None or str values. '
                  'Supplying anything different as a default may cause bugs. '
                  'See https://docs.python.org/3/library/os.html#os.putenv. '),
    }

    deprecated = {
        0: [
            'cgi.parse_qs', 'cgi.parse_qsl',
            'ctypes.c_buffer',
            'distutils.command.register.register.check_metadata',
            'distutils.command.sdist.sdist.check_metadata',
            'tkinter.Misc.tk_menuBar',
            'tkinter.Menu.tk_bindForTraversal',
        ],
        2: {
            (2, 6, 0): [
                'commands.getstatus',
                'os.popen2',
                'os.popen3',
                'os.popen4',
                'macostools.touched',
            ],
            (2, 7, 0): [
                'unittest.case.TestCase.assertEquals',
                'unittest.case.TestCase.assertNotEquals',
                'unittest.case.TestCase.assertAlmostEquals',
                'unittest.case.TestCase.assertNotAlmostEquals',
                'unittest.case.TestCase.assert_',
                'xml.etree.ElementTree.Element.getchildren',
                'xml.etree.ElementTree.Element.getiterator',
                'xml.etree.ElementTree.XMLParser.getiterator',
                'xml.etree.ElementTree.XMLParser.doctype',
            ],
        },
        3: {
            (3, 0, 0): [
                'inspect.getargspec',
                'unittest.case.TestCase._deprecate.deprecated_func',
            ],
            (3, 1, 0): [
                'base64.encodestring', 'base64.decodestring',
                'ntpath.splitunc',
            ],
            (3, 2, 0): [
                'cgi.escape',
                'configparser.RawConfigParser.readfp',
                'xml.etree.ElementTree.Element.getchildren',
                'xml.etree.ElementTree.Element.getiterator',
                'xml.etree.ElementTree.XMLParser.getiterator',
                'xml.etree.ElementTree.XMLParser.doctype',
            ],
            (3, 3, 0): [
                'inspect.getmoduleinfo',
                'logging.warn', 'logging.Logger.warn',
                'logging.LoggerAdapter.warn',
                'nntplib._NNTPBase.xpath',
                'platform.popen',
            ],
            (3, 4, 0): [
                'importlib.find_loader',
                'plistlib.readPlist', 'plistlib.writePlist',
                'plistlib.readPlistFromBytes',
                'plistlib.writePlistToBytes',
            ],
            (3, 4, 4): [
                'asyncio.tasks.async',
            ],
            (3, 5, 0): [
                'fractions.gcd',
                'inspect.getargvalues',
                'inspect.formatargspec', 'inspect.formatargvalues',
                'inspect.getcallargs',
                'platform.linux_distribution', 'platform.dist',
            ],
            (3, 6, 0): [
                'importlib._bootstrap_external.FileLoader.load_module',
            ],
        },
    }

    def _check_bad_thread_instantiation(self, node):
        if not node.kwargs and not node.keywords and len(node.args) <= 1:
            self.add_message('bad-thread-instantiation', node=node)

    def _check_shallow_copy_environ(self, node):
        arg = utils.get_argument_from_call(node, position=0)
        for inferred in arg.inferred():
            if inferred.qname() == OS_ENVIRON:
                self.add_message('shallow-copy-environ', node=node)
                break

    @utils.check_messages('bad-open-mode', 'redundant-unittest-assert',
                          'deprecated-method',
                          'bad-thread-instantiation',
                          'shallow-copy-environ')
    def visit_call(self, node):
        """Visit a Call node."""
        try:
            for inferred in node.func.infer():
                if inferred is astroid.Uninferable:
                    continue
                elif inferred.root().name == OPEN_MODULE:
                    if getattr(node.func, 'name', None) in OPEN_FILES:
                        self._check_open_mode(node)
                elif inferred.root().name == UNITTEST_CASE:
                    self._check_redundant_assert(node, inferred)
                elif isinstance(inferred, astroid.ClassDef) and inferred.qname() == THREADING_THREAD:
                    self._check_bad_thread_instantiation(node)
                elif isinstance(inferred, astroid.FunctionDef) and inferred.qname() == COPY_COPY:
                    self._check_shallow_copy_environ(node)
                elif inferred.qname() in ENV_FUNCTIONS:
                    self._check_env_function(node, inferred)
                self._check_deprecated_method(node, inferred)
        except astroid.InferenceError:
            return

    @utils.check_messages('boolean-datetime')
    def visit_unaryop(self, node):
        if node.op == 'not':
            self._check_datetime(node.operand)

    @utils.check_messages('boolean-datetime')
    def visit_if(self, node):
        self._check_datetime(node.test)

    @utils.check_messages('boolean-datetime')
    def visit_ifexp(self, node):
        self._check_datetime(node.test)

    @utils.check_messages('boolean-datetime')
    def visit_boolop(self, node):
        for value in node.values:
            self._check_datetime(value)

    def _check_deprecated_method(self, node, inferred):
        py_vers = sys.version_info[0]

        if isinstance(node.func, astroid.Attribute):
            func_name = node.func.attrname
        elif isinstance(node.func, astroid.Name):
            func_name = node.func.name
        else:
            # Not interested in other nodes.
            return

        # Reject nodes which aren't of interest to us.
        acceptable_nodes = (astroid.BoundMethod,
                            astroid.UnboundMethod,
                            astroid.FunctionDef)
        if not isinstance(inferred, acceptable_nodes):
            return

        qname = inferred.qname()
        if qname in self.deprecated[0]:
            self.add_message('deprecated-method', node=node,
                             args=(func_name, ))
        else:
            for since_vers, func_list in self.deprecated[py_vers].items():
                if since_vers <= sys.version_info and qname in func_list:
                    self.add_message('deprecated-method', node=node,
                                     args=(func_name, ))
                    break

    def _check_redundant_assert(self, node, infer):
        if (isinstance(infer, astroid.BoundMethod) and
                node.args and isinstance(node.args[0], astroid.Const) and
                infer.name in ['assertTrue', 'assertFalse']):
            self.add_message('redundant-unittest-assert',
                             args=(infer.name, node.args[0].value, ),
                             node=node)

    def _check_datetime(self, node):
        """ Check that a datetime was infered.
        If so, emit boolean-datetime warning.
        """
        try:
            infered = next(node.infer())
        except astroid.InferenceError:
            return
        if (isinstance(infered, Instance) and
                infered.qname() == 'datetime.time'):
            self.add_message('boolean-datetime', node=node)

    def _check_open_mode(self, node):
        """Check that the mode argument of an open or file call is valid."""
        try:
            mode_arg = utils.get_argument_from_call(node, position=1,
                                                    keyword='mode')
        except utils.NoSuchArgumentError:
            return
        if mode_arg:
            mode_arg = utils.safe_infer(mode_arg)
            if (isinstance(mode_arg, astroid.Const)
                    and not _check_mode_str(mode_arg.value)):
                self.add_message('bad-open-mode', node=node,
                                 args=mode_arg.value)

    def _check_env_function(self, node, infer):
        if node.keywords:
            kwargs = {keyword.arg: keyword.value for keyword in node.keywords}
        else:
            kwargs = None

        if infer.qname() in ENV_SETTERS:
            env_name_kwarg = 'name'
            env_value_kwarg = 'value'
            value_is_default = False
        else:
            env_name_kwarg = 'key'
            env_value_kwarg = 'default'
            value_is_default = True

        if len(node.args) > 0:
            env_name_arg = node.args[0]
        elif kwargs and env_name_kwarg in kwargs:
            env_name_arg = kwargs[env_name_kwarg]
        else:
            env_name_arg = None

        if env_name_arg:
            self._check_invalid_envvar_value(
                node=node,
                message='invalid-envvar-value',
                call_arg=utils.safe_infer(env_name_arg),
                infer=infer,
                allow_none=False
            )

        if len(node.args) == 2:
            env_value_arg = node.args[1]
        elif kwargs and env_value_kwarg in kwargs:
            env_value_arg = kwargs[env_value_kwarg]
        else:
            env_value_arg = None

        if env_value_arg:
            self._check_invalid_envvar_value(
                node=node,
                infer=infer,
                message='invalid-envvar-default' if value_is_default else 'invalid-envvar-value',
                call_arg=utils.safe_infer(env_value_arg),
                allow_none=value_is_default
            )

    def _check_invalid_envvar_value(self, node, infer, message, call_arg, allow_none):

        if call_arg is astroid.Uninferable:
            return

        if isinstance(call_arg, Const):
            if not (isinstance(call_arg.value, six.text_type) or (not allow_none and call_arg.value is None)):
                self.add_message(message, node=node, args=(infer.qname(), call_arg.pytype()))
        else:
            self.add_message(message, node=node, args=(infer.qname(), call_arg.pytype()))


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(StdlibChecker(linter))
