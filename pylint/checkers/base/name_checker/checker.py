# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Basic checker for Python code."""
import collections
import itertools
import re
import sys
from typing import Dict, Optional, Pattern, Tuple

import astroid
from astroid import nodes

from pylint import constants, interfaces
from pylint.checkers import utils
from pylint.checkers.base.basic_checker import _BasicChecker
from pylint.checkers.base.name_checker.naming_style import (
    KNOWN_NAME_TYPES,
    KNOWN_NAME_TYPES_WITH_STYLE,
    NAMING_STYLES,
    _create_naming_options,
)
from pylint.checkers.utils import is_property_deleter, is_property_setter

# Default patterns for name types that do not have styles
DEFAULT_PATTERNS = {
    "typevar": re.compile(
        r"^_{0,2}(?:[^\W\da-z_]+|(?:[^\W\da-z_][^\WA-Z_]+)+T?(?<!Type))(?:_co(?:ntra)?)?$"
    )
}

BUILTIN_PROPERTY = "builtins.property"
TYPING_TYPE_VAR_QNAME = "typing.TypeVar"


def _get_properties(config):
    """Returns a tuple of property classes and names.

    Property classes are fully qualified, such as 'abc.abstractproperty' and
    property names are the actual names, such as 'abstract_property'.
    """
    property_classes = {BUILTIN_PROPERTY}
    property_names = set()  # Not returning 'property', it has its own check.
    if config is not None:
        property_classes.update(config.property_classes)
        property_names.update(
            prop.rsplit(".", 1)[-1] for prop in config.property_classes
        )
    return property_classes, property_names


def _redefines_import(node):
    """Detect that the given node (AssignName) is inside an
    exception handler and redefines an import from the tryexcept body.

    Returns True if the node redefines an import, False otherwise.
    """
    current = node
    while current and not isinstance(current.parent, nodes.ExceptHandler):
        current = current.parent
    if not current or not utils.error_of_type(current.parent, ImportError):
        return False
    try_block = current.parent.parent
    for import_node in try_block.nodes_of_class((nodes.ImportFrom, nodes.Import)):
        for name, alias in import_node.names:
            if alias:
                if alias == node.name:
                    return True
            elif name == node.name:
                return True
    return False


def _determine_function_name_type(node: nodes.FunctionDef, config=None):
    """Determine the name type whose regex the function's name should match.

    :param node: A function node.
    :param config: Configuration from which to pull additional property classes.
    :type config: :class:`optparse.Values`

    :returns: One of ('function', 'method', 'attr')
    :rtype: str
    """
    property_classes, property_names = _get_properties(config)
    if not node.is_method():
        return "function"

    if is_property_setter(node) or is_property_deleter(node):
        # If the function is decorated using the prop_method.{setter,getter}
        # form, treat it like an attribute as well.
        return "attr"

    decorators = node.decorators.nodes if node.decorators else []
    for decorator in decorators:
        # If the function is a property (decorated with @property
        # or @abc.abstractproperty), the name type is 'attr'.
        if isinstance(decorator, nodes.Name) or (
            isinstance(decorator, nodes.Attribute)
            and decorator.attrname in property_names
        ):
            inferred = utils.safe_infer(decorator)
            if (
                inferred
                and hasattr(inferred, "qname")
                and inferred.qname() in property_classes
            ):
                return "attr"
    return "method"


# Name categories that are always consistent with all naming conventions.
EXEMPT_NAME_CATEGORIES = {"exempt", "ignore"}


def _is_multi_naming_match(match, node_type, confidence):
    return (
        match is not None
        and match.lastgroup is not None
        and match.lastgroup not in EXEMPT_NAME_CATEGORIES
        and (node_type != "method" or confidence != interfaces.INFERENCE_FAILURE)
    )


class NameChecker(_BasicChecker):
    msgs = {
        "C0103": (
            '%s name "%s" doesn\'t conform to %s',
            "invalid-name",
            "Used when the name doesn't conform to naming rules "
            "associated to its type (constant, variable, class...).",
        ),
        "C0104": (
            'Disallowed name "%s"',
            "disallowed-name",
            "Used when the name matches bad-names or bad-names-rgxs- (unauthorized names).",
            {
                "old_names": [
                    ("C0102", "blacklisted-name"),
                ]
            },
        ),
        "C0105": (
            'Type variable "%s" is %s, use "%s" instead',
            "typevar-name-incorrect-variance",
            "Emitted when a TypeVar name doesn't reflect its type variance. "
            "According to PEP8, it is recommended to add suffixes '_co' and "
            "'_contra' to the variables used to declare covariant or "
            "contravariant behaviour respectively. Invariant (default) variables "
            "do not require a suffix. The message is also emitted when invariant "
            "variables do have a suffix.",
        ),
        "W0111": (
            "Name %s will become a keyword in Python %s",
            "assign-to-new-keyword",
            "Used when assignment will become invalid in future "
            "Python release due to introducing new keyword.",
        ),
    }

    options = (
        (
            "good-names",
            {
                "default": ("i", "j", "k", "ex", "Run", "_"),
                "type": "csv",
                "metavar": "<names>",
                "help": "Good variable names which should always be accepted,"
                " separated by a comma.",
            },
        ),
        (
            "good-names-rgxs",
            {
                "default": "",
                "type": "regexp_csv",
                "metavar": "<names>",
                "help": "Good variable names regexes, separated by a comma. If names match any regex,"
                " they will always be accepted",
            },
        ),
        (
            "bad-names",
            {
                "default": ("foo", "bar", "baz", "toto", "tutu", "tata"),
                "type": "csv",
                "metavar": "<names>",
                "help": "Bad variable names which should always be refused, "
                "separated by a comma.",
            },
        ),
        (
            "bad-names-rgxs",
            {
                "default": "",
                "type": "regexp_csv",
                "metavar": "<names>",
                "help": "Bad variable names regexes, separated by a comma. If names match any regex,"
                " they will always be refused",
            },
        ),
        (
            "name-group",
            {
                "default": (),
                "type": "csv",
                "metavar": "<name1:name2>",
                "help": (
                    "Colon-delimited sets of names that determine each"
                    " other's naming style when the name regexes"
                    " allow several styles."
                ),
            },
        ),
        (
            "include-naming-hint",
            {
                "default": False,
                "type": "yn",
                "metavar": "<y or n>",
                "help": "Include a hint for the correct naming format with invalid-name.",
            },
        ),
        (
            "property-classes",
            {
                "default": ("abc.abstractproperty",),
                "type": "csv",
                "metavar": "<decorator names>",
                "help": "List of decorators that produce properties, such as "
                "abc.abstractproperty. Add to this list to register "
                "other decorators that produce valid properties. "
                "These decorators are taken in consideration only for invalid-name.",
            },
        ),
    ) + _create_naming_options()

    KEYWORD_ONSET = {(3, 7): {"async", "await"}}

    def __init__(self, linter):
        super().__init__(linter)
        self._name_category = {}
        self._name_group = {}
        self._bad_names = {}
        self._name_regexps = {}
        self._name_hints = {}
        self._good_names_rgxs_compiled = []
        self._bad_names_rgxs_compiled = []

    def open(self):
        self.linter.stats.reset_bad_names()
        for group in self.config.name_group:
            for name_type in group.split(":"):
                self._name_group[name_type] = f"group_{group}"

        regexps, hints = self._create_naming_rules()
        self._name_regexps = regexps
        self._name_hints = hints
        self._good_names_rgxs_compiled = [
            re.compile(rgxp) for rgxp in self.config.good_names_rgxs
        ]
        self._bad_names_rgxs_compiled = [
            re.compile(rgxp) for rgxp in self.config.bad_names_rgxs
        ]

    def _create_naming_rules(self) -> Tuple[Dict[str, Pattern[str]], Dict[str, str]]:
        regexps: Dict[str, Pattern[str]] = {}
        hints: Dict[str, str] = {}

        for name_type in KNOWN_NAME_TYPES:
            if name_type in KNOWN_NAME_TYPES_WITH_STYLE:
                naming_style_name = getattr(self.config, f"{name_type}_naming_style")
                regexps[name_type] = NAMING_STYLES[naming_style_name].get_regex(
                    name_type
                )
            else:
                naming_style_name = "predefined"
                regexps[name_type] = DEFAULT_PATTERNS[name_type]

            custom_regex_setting_name = f"{name_type}_rgx"
            custom_regex = getattr(self.config, custom_regex_setting_name, None)
            if custom_regex is not None:
                regexps[name_type] = custom_regex

            if custom_regex is not None:
                hints[name_type] = f"{custom_regex.pattern!r} pattern"
            else:
                hints[name_type] = f"{naming_style_name} naming style"

        return regexps, hints

    @utils.check_messages("disallowed-name", "invalid-name")
    def visit_module(self, node: nodes.Module) -> None:
        self._check_name("module", node.name.split(".")[-1], node)
        self._bad_names = {}

    def leave_module(self, _: nodes.Module) -> None:
        for all_groups in self._bad_names.values():
            if len(all_groups) < 2:
                continue
            groups = collections.defaultdict(list)
            min_warnings = sys.maxsize
            prevalent_group, _ = max(all_groups.items(), key=lambda item: len(item[1]))
            for group in all_groups.values():
                groups[len(group)].append(group)
                min_warnings = min(len(group), min_warnings)
            if len(groups[min_warnings]) > 1:
                by_line = sorted(
                    groups[min_warnings],
                    key=lambda group: min(warning[0].lineno for warning in group),
                )
                warnings = itertools.chain(*by_line[1:])
            else:
                warnings = groups[min_warnings][0]
            for args in warnings:
                self._raise_name_warning(prevalent_group, *args)

    @utils.check_messages("disallowed-name", "invalid-name", "assign-to-new-keyword")
    def visit_classdef(self, node: nodes.ClassDef) -> None:
        self._check_assign_to_new_keyword_violation(node.name, node)
        self._check_name("class", node.name, node)
        for attr, anodes in node.instance_attrs.items():
            if not any(node.instance_attr_ancestors(attr)):
                self._check_name("attr", attr, anodes[0])

    @utils.check_messages("disallowed-name", "invalid-name", "assign-to-new-keyword")
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        # Do not emit any warnings if the method is just an implementation
        # of a base class method.
        self._check_assign_to_new_keyword_violation(node.name, node)
        confidence = interfaces.HIGH
        if node.is_method():
            if utils.overrides_a_method(node.parent.frame(future=True), node.name):
                return
            confidence = (
                interfaces.INFERENCE
                if utils.has_known_bases(node.parent.frame(future=True))
                else interfaces.INFERENCE_FAILURE
            )

        self._check_name(
            _determine_function_name_type(node, config=self.config),
            node.name,
            node,
            confidence,
        )
        # Check argument names
        args = node.args.args
        if args is not None:
            self._recursive_check_names(args)

    visit_asyncfunctiondef = visit_functiondef

    @utils.check_messages("disallowed-name", "invalid-name")
    def visit_global(self, node: nodes.Global) -> None:
        for name in node.names:
            self._check_name("const", name, node)

    @utils.check_messages(
        "disallowed-name",
        "invalid-name",
        "assign-to-new-keyword",
        "typevar-name-incorrect-variance",
    )
    def visit_assignname(self, node: nodes.AssignName) -> None:
        """Check module level assigned names."""
        self._check_assign_to_new_keyword_violation(node.name, node)
        frame = node.frame(future=True)
        assign_type = node.assign_type()

        # Check names defined in comprehensions
        if isinstance(assign_type, nodes.Comprehension):
            self._check_name("inlinevar", node.name, node)

        # Check names defined in module scope
        elif isinstance(frame, nodes.Module):
            # Check names defined in Assign nodes
            if isinstance(assign_type, nodes.Assign):
                inferred_assign_type = utils.safe_infer(assign_type.value)

                # Check TypeVar's assigned alone or in tuple assignment
                if isinstance(node.parent, nodes.Assign) and self._assigns_typevar(
                    assign_type.value
                ):
                    self._check_name("typevar", assign_type.targets[0].name, node)
                elif (
                    isinstance(node.parent, nodes.Tuple)
                    and isinstance(assign_type.value, nodes.Tuple)
                    and self._assigns_typevar(
                        assign_type.value.elts[node.parent.elts.index(node)]
                    )
                ):
                    self._check_name(
                        "typevar",
                        assign_type.targets[0].elts[node.parent.elts.index(node)].name,
                        node,
                    )

                # Check classes (TypeVar's are classes so they need to be excluded first)
                elif isinstance(inferred_assign_type, nodes.ClassDef):
                    self._check_name("class", node.name, node)

                # Don't emit if the name redefines an import in an ImportError except handler.
                elif not _redefines_import(node) and isinstance(
                    inferred_assign_type, nodes.Const
                ):
                    self._check_name("const", node.name, node)
            # Check names defined in AnnAssign nodes
            elif isinstance(
                assign_type, nodes.AnnAssign
            ) and utils.is_assign_name_annotated_with(node, "Final"):
                self._check_name("const", node.name, node)

        # Check names defined in function scopes
        elif isinstance(frame, nodes.FunctionDef):
            # global introduced variable aren't in the function locals
            if node.name in frame and node.name not in frame.argnames():
                if not _redefines_import(node):
                    self._check_name("variable", node.name, node)

        # Check names defined in class scopes
        elif isinstance(frame, nodes.ClassDef):
            if not list(frame.local_attr_ancestors(node.name)):
                for ancestor in frame.ancestors():
                    if (
                        ancestor.name == "Enum"
                        and ancestor.root().name == "enum"
                        or utils.is_assign_name_annotated_with(node, "Final")
                    ):
                        self._check_name("class_const", node.name, node)
                        break
                else:
                    self._check_name("class_attribute", node.name, node)

    def _recursive_check_names(self, args):
        """Check names in a possibly recursive list <arg>."""
        for arg in args:
            if isinstance(arg, nodes.AssignName):
                self._check_name("argument", arg.name, arg)
            else:
                self._recursive_check_names(arg.elts)

    def _find_name_group(self, node_type):
        return self._name_group.get(node_type, node_type)

    def _raise_name_warning(
        self,
        prevalent_group: Optional[str],
        node: nodes.NodeNG,
        node_type: str,
        name: str,
        confidence,
        warning: str = "invalid-name",
    ) -> None:
        type_label = constants.HUMAN_READABLE_TYPES[node_type]
        hint = self._name_hints[node_type]
        if prevalent_group:
            # This happens in the multi naming match case. The expected
            # prevalent group needs to be spelled out to make the message
            # correct.
            hint = f"the `{prevalent_group}` group in the {hint}"
        if self.config.include_naming_hint:
            hint += f" ({self._name_regexps[node_type].pattern!r} pattern)"
        args = (
            (type_label.capitalize(), name, hint)
            if warning == "invalid-name"
            else (type_label.capitalize(), name)
        )

        self.add_message(warning, node=node, args=args, confidence=confidence)
        self.linter.stats.increase_bad_name(node_type, 1)

    def _name_allowed_by_regex(self, name: str) -> bool:
        return name in self.config.good_names or any(
            pattern.match(name) for pattern in self._good_names_rgxs_compiled
        )

    def _name_disallowed_by_regex(self, name: str) -> bool:
        return name in self.config.bad_names or any(
            pattern.match(name) for pattern in self._bad_names_rgxs_compiled
        )

    def _check_name(self, node_type, name, node, confidence=interfaces.HIGH):
        """Check for a name using the type's regexp."""

        def _should_exempt_from_invalid_name(node):
            if node_type == "variable":
                inferred = utils.safe_infer(node)
                if isinstance(inferred, nodes.ClassDef):
                    return True
            return False

        if self._name_allowed_by_regex(name=name):
            return
        if self._name_disallowed_by_regex(name=name):
            self.linter.stats.increase_bad_name(node_type, 1)
            self.add_message("disallowed-name", node=node, args=name)
            return
        regexp = self._name_regexps[node_type]
        match = regexp.match(name)

        if _is_multi_naming_match(match, node_type, confidence):
            name_group = self._find_name_group(node_type)
            bad_name_group = self._bad_names.setdefault(name_group, {})
            warnings = bad_name_group.setdefault(match.lastgroup, [])
            warnings.append((node, node_type, name, confidence))

        if match is None and not _should_exempt_from_invalid_name(node):
            self._raise_name_warning(None, node, node_type, name, confidence)

        # Check TypeVar names for variance suffixes
        if node_type == "typevar":
            self._check_typevar_variance(name, node)

    def _check_assign_to_new_keyword_violation(self, name, node):
        keyword_first_version = self._name_became_keyword_in_version(
            name, self.KEYWORD_ONSET
        )
        if keyword_first_version is not None:
            self.add_message(
                "assign-to-new-keyword",
                node=node,
                args=(name, keyword_first_version),
                confidence=interfaces.HIGH,
            )

    @staticmethod
    def _name_became_keyword_in_version(name, rules):
        for version, keywords in rules.items():
            if name in keywords and sys.version_info < version:
                return ".".join(str(v) for v in version)
        return None

    @staticmethod
    def _assigns_typevar(node: Optional[nodes.NodeNG]) -> bool:
        """Check if a node is assigning a TypeVar."""
        if isinstance(node, astroid.Call):
            inferred = utils.safe_infer(node.func)
            if (
                isinstance(inferred, astroid.ClassDef)
                and inferred.qname() == TYPING_TYPE_VAR_QNAME
            ):
                return True
        return False

    def _check_typevar_variance(self, name: str, node: nodes.AssignName) -> None:
        """Check if a TypeVar has a variance and if it's included in the name.

        Returns the args for the message to be displayed.
        """
        if isinstance(node.parent, nodes.Assign):
            keywords = node.assign_type().value.keywords
        elif isinstance(node.parent, nodes.Tuple):
            keywords = (
                node.assign_type().value.elts[node.parent.elts.index(node)].keywords
            )

        for kw in keywords:
            if kw.arg == "covariant" and kw.value.value:
                if not name.endswith("_co"):
                    suggest_name = f"{re.sub('_contra$', '', name)}_co"
                    self.add_message(
                        "typevar-name-incorrect-variance",
                        node=node,
                        args=(name, "covariant", suggest_name),
                        confidence=interfaces.INFERENCE,
                    )
                return

            if kw.arg == "contravariant" and kw.value.value:
                if not name.endswith("_contra"):
                    suggest_name = f"{re.sub('_co$', '', name)}_contra"
                    self.add_message(
                        "typevar-name-incorrect-variance",
                        node=node,
                        args=(name, "contravariant", suggest_name),
                        confidence=interfaces.INFERENCE,
                    )
                return

        if name.endswith("_co") or name.endswith("_contra"):
            suggest_name = re.sub("_contra$|_co$", "", name)
            self.add_message(
                "typevar-name-incorrect-variance",
                node=node,
                args=(name, "invariant", suggest_name),
                confidence=interfaces.INFERENCE,
            )
