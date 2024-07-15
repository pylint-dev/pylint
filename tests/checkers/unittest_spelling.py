# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unittest for the spelling checker."""

import astroid
import pytest

from pylint.checkers import spelling
from pylint.checkers.spelling import _get_enchant_dict_help
from pylint.testutils import CheckerTestCase, MessageTest, _tokenize_str, set_config

# try to create enchant dictionary
try:
    import enchant
except ImportError:
    enchant = None

spell_dict = None
if enchant is not None:
    try:
        enchant.Dict("en_US")
        spell_dict = "en_US"
    except enchant.DictNotFoundError:
        pass


class TestSpellingChecker(CheckerTestCase):  # pylint:disable=too-many-public-methods
    # This is a test case class, not sure why it would be relevant to have
    #   this pylint rule enforced for test case classes.
    CHECKER_CLASS = spelling.SpellingChecker

    skip_on_missing_package_or_dict = pytest.mark.skipif(
        spell_dict is None,
        reason="missing python-enchant package or missing spelling dictionaries",
    )

    def _get_msg_suggestions(self, word: str, count: int = 4) -> str:
        suggestions = "' or '".join(self.checker.spelling_dict.suggest(word)[:count])
        return f"'{suggestions}'"

    def test_spelling_dict_help_no_enchant(self) -> None:
        assert "both the python package and the system dep" in _get_enchant_dict_help(
            [], pyenchant_available=False
        )
        assert "need to install the system dep" in _get_enchant_dict_help(
            [], pyenchant_available=True
        )

    @skip_on_missing_package_or_dict
    def test_spelling_dict_help_enchant(self) -> None:
        assert "Available dictionaries: " in _get_enchant_dict_help(
            enchant.Broker().list_dicts(), pyenchant_available=True
        )

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_check_bad_coment(self) -> None:
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-comment",
                line=1,
                args=(
                    "coment",
                    "# bad coment",
                    "      ^^^^^^",
                    self._get_msg_suggestions("coment"),
                ),
            )
        ):
            self.checker.process_tokens(_tokenize_str("# bad coment"))

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    @set_config(max_spelling_suggestions=2)
    def test_check_bad_comment_custom_suggestion_count(self) -> None:
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-comment",
                line=1,
                args=(
                    "coment",
                    "# bad coment",
                    "      ^^^^^^",
                    self._get_msg_suggestions("coment", count=2),
                ),
            )
        ):
            self.checker.process_tokens(_tokenize_str("# bad coment"))

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_check_bad_docstring(self) -> None:
        stmt = astroid.extract_node('def fff():\n   """bad coment"""\n   pass')
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=2,
                args=(
                    "coment",
                    "bad coment",
                    "    ^^^^^^",
                    self._get_msg_suggestions("coment"),
                ),
            )
        ):
            self.checker.visit_functiondef(stmt)

        stmt = astroid.extract_node('class Abc(object):\n   """bad coment"""\n   pass')
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=2,
                args=(
                    "coment",
                    "bad coment",
                    "    ^^^^^^",
                    self._get_msg_suggestions("coment"),
                ),
            )
        ):
            self.checker.visit_classdef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_shebangs(self) -> None:
        self.checker.process_tokens(_tokenize_str("#!/usr/bin/env python"))
        assert not self.linter.release_messages()

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_python_coding_comments(self) -> None:
        self.checker.process_tokens(_tokenize_str("# -*- coding: utf-8 -*-"))
        assert not self.linter.release_messages()
        self.checker.process_tokens(_tokenize_str("# coding=utf-8"))
        assert not self.linter.release_messages()
        self.checker.process_tokens(_tokenize_str("# vim: set fileencoding=utf-8 :"))
        assert not self.linter.release_messages()
        # Now with a shebang first
        self.checker.process_tokens(
            _tokenize_str("#!/usr/bin/env python\n# -*- coding: utf-8 -*-")
        )
        assert not self.linter.release_messages()
        self.checker.process_tokens(
            _tokenize_str("#!/usr/bin/env python\n# coding=utf-8")
        )
        assert not self.linter.release_messages()
        self.checker.process_tokens(
            _tokenize_str("#!/usr/bin/env python\n# vim: set fileencoding=utf-8 :")
        )
        assert not self.linter.release_messages()

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_top_level_pylint_enable_disable_comments(self) -> None:
        self.checker.process_tokens(
            _tokenize_str("# Line 1\n Line 2\n# pylint: disable=ungrouped-imports")
        )
        assert not self.linter.release_messages()

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_words_with_numbers(self) -> None:
        self.checker.process_tokens(_tokenize_str("\n# 0ne\n# Thr33\n# Sh3ll"))
        assert not self.linter.release_messages()

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_wiki_words(self) -> None:
        stmt = astroid.extract_node(
            'class ComentAbc(object):\n   """ComentAbc with a bad coment"""\n   pass'
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=2,
                args=(
                    "coment",
                    "ComentAbc with a bad coment",
                    "                     ^^^^^^",
                    self._get_msg_suggestions("coment"),
                ),
            )
        ):
            self.checker.visit_classdef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_camel_cased_words(self) -> None:
        stmt = astroid.extract_node(
            'class ComentAbc(object):\n   """comentAbc with a bad coment"""\n   pass'
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=2,
                args=(
                    "coment",
                    "comentAbc with a bad coment",
                    "                     ^^^^^^",
                    self._get_msg_suggestions("coment"),
                ),
            )
        ):
            self.checker.visit_classdef(stmt)

        # With just a single upper case letter in the end
        stmt = astroid.extract_node(
            'class ComentAbc(object):\n   """argumentN with a bad coment"""\n   pass'
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=2,
                args=(
                    "coment",
                    "argumentN with a bad coment",
                    "                     ^^^^^^",
                    self._get_msg_suggestions("coment"),
                ),
            )
        ):
            self.checker.visit_classdef(stmt)

        for ccn in (
            "xmlHttpRequest",
            "newCustomer",
            "newCustomerId",
            "innerStopwatch",
            "supportsIpv6OnIos",
            "affine3D",
        ):
            stmt = astroid.extract_node(
                f'class TestClass(object):\n   """{ccn} comment"""\n   pass'
            )
            self.checker.visit_classdef(stmt)
            assert not self.linter.release_messages()

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_words_with_underscores(self) -> None:
        stmt = astroid.extract_node(
            'def fff(param_name):\n   """test param_name"""\n   pass'
        )
        self.checker.visit_functiondef(stmt)
        assert not self.linter.release_messages()

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_email_address(self) -> None:
        self.checker.process_tokens(_tokenize_str("# uname@domain.tld"))
        assert not self.linter.release_messages()

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_urls(self) -> None:
        self.checker.process_tokens(_tokenize_str("# https://github.com/rfk/pyenchant"))
        assert not self.linter.release_messages()

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    @pytest.mark.parametrize(
        "type_comment",
        [
            "# type: (NotAWord) -> NotAWord",
            "# type: List[NotAWord] -> List[NotAWord]",
            "# type: Dict[NotAWord] -> Dict[NotAWord]",
            "# type: NotAWord",
            "# type: List[NotAWord]",
            "# type: Dict[NotAWord]",
            "# type: ImmutableList[Manager]",
            # will result in error: Invalid "type: ignore" comment  [syntax]
            # when analyzed with mypy 1.02
            "# type: ignore[attr-defined] NotAWord",
        ],
    )
    def test_skip_type_comments(self, type_comment: str) -> None:
        self.checker.process_tokens(_tokenize_str(type_comment))
        assert not self.linter.release_messages()

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_sphinx_directives(self) -> None:
        stmt = astroid.extract_node(
            'class ComentAbc(object):\n   """This is :class:`ComentAbc` with a bad coment"""\n   pass'
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=2,
                args=(
                    "coment",
                    "This is :class:`ComentAbc` with a bad coment",
                    "                                      ^^^^^^",
                    self._get_msg_suggestions("coment"),
                ),
            )
        ):
            self.checker.visit_classdef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_sphinx_directives_2(self) -> None:
        stmt = astroid.extract_node(
            'class ComentAbc(object):\n   """This is :py:attr:`ComentAbc` with a bad coment"""\n   pass'
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=2,
                args=(
                    "coment",
                    "This is :py:attr:`ComentAbc` with a bad coment",
                    "                                        ^^^^^^",
                    self._get_msg_suggestions("coment"),
                ),
            )
        ):
            self.checker.visit_classdef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    @pytest.mark.parametrize(
        "prefix,suffix",
        (
            pytest.param("fmt", ": on", id="black directive to turn on formatting"),
            pytest.param("fmt", ": off", id="black directive to turn off formatting"),
            pytest.param("noqa", "", id="pycharm directive"),
            pytest.param("noqa", ":", id="flake8 / zimports directive"),
            pytest.param("nosec", "", id="bandit directive"),
            pytest.param("isort", ":skip", id="isort directive"),
            pytest.param("mypy", ":", id="mypy top of file directive"),
        ),
    )
    def test_tool_directives_handling(self, prefix: str, suffix: str) -> None:
        """We're not raising when the directive is at the beginning of comments,
        but we raise if a directive appears later in comment.
        """
        full_comment = f"# {prefix}{suffix} {prefix}"
        args = (
            prefix,
            full_comment,
            f"  {'^' * len(prefix)}",
            self._get_msg_suggestions(prefix),
        )
        with self.assertAddsMessages(
            MessageTest("wrong-spelling-in-comment", line=1, args=args)
        ):
            self.checker.process_tokens(_tokenize_str(full_comment))

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_code_flanked_in_double_backticks(self) -> None:
        full_comment = "# The function ``.qsize()`` .qsize()"
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-comment",
                line=1,
                args=(
                    "qsize",
                    full_comment,
                    "                 ^^^^^",
                    self._get_msg_suggestions("qsize"),
                ),
            )
        ):
            self.checker.process_tokens(_tokenize_str(full_comment))

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_skip_code_flanked_in_single_backticks(self) -> None:
        full_comment = "# The function `.qsize()` .qsize()"
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-comment",
                line=1,
                args=(
                    "qsize",
                    full_comment,
                    "                 ^^^^^",
                    self._get_msg_suggestions("qsize"),
                ),
            )
        ):
            self.checker.process_tokens(_tokenize_str(full_comment))

    @skip_on_missing_package_or_dict
    @set_config(
        spelling_dict=spell_dict,
        spelling_ignore_comment_directives="newdirective:,noqa",
    )
    def test_skip_directives_specified_in_pylintrc(self) -> None:
        full_comment = "# newdirective: do this newdirective"
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-comment",
                line=1,
                args=(
                    "newdirective",
                    full_comment,
                    "          ^^^^^^^^^^^^",
                    self._get_msg_suggestions("newdirective"),
                ),
            )
        ):
            self.checker.process_tokens(_tokenize_str(full_comment))

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_handle_words_joined_by_forward_slash(self) -> None:
        stmt = astroid.extract_node(
            '''
        class ComentAbc(object):
            """This is Comment/Abcz with a bad comment"""
            pass
        '''
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=3,
                args=(
                    "Abcz",
                    "This is Comment/Abcz with a bad comment",
                    "                ^^^^",
                    self._get_msg_suggestions("Abcz"),
                ),
            )
        ):
            self.checker.visit_classdef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_more_than_one_error_in_same_line_for_same_word_on_docstring(self) -> None:
        stmt = astroid.extract_node(
            'class ComentAbc(object):\n   """Check teh dummy comment teh"""\n   pass'
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=2,
                args=(
                    "teh",
                    "Check teh dummy comment teh",
                    "      ^^^",
                    self._get_msg_suggestions("teh"),
                ),
            ),
            MessageTest(
                "wrong-spelling-in-docstring",
                line=2,
                args=(
                    "teh",
                    "Check teh dummy comment teh",
                    "                        ^^^",
                    self._get_msg_suggestions("teh"),
                ),
            ),
        ):
            self.checker.visit_classdef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_more_than_one_error_in_same_line_for_same_word_on_comment(self) -> None:
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-comment",
                line=1,
                args=(
                    "coment",
                    "# bad coment coment",
                    "      ^^^^^^",
                    self._get_msg_suggestions("coment"),
                ),
            ),
            MessageTest(
                "wrong-spelling-in-comment",
                line=1,
                args=(
                    "coment",
                    "# bad coment coment",
                    "             ^^^^^^",
                    self._get_msg_suggestions("coment"),
                ),
            ),
        ):
            self.checker.process_tokens(_tokenize_str("# bad coment coment"))

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_docstring_lines_that_look_like_comments_1(self) -> None:
        stmt = astroid.extract_node(
            '''def f():
    """
    # msitake
    """'''
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=3,
                args=(
                    "msitake",
                    "    # msitake",
                    "      ^^^^^^^",
                    self._get_msg_suggestions("msitake"),
                ),
            )
        ):
            self.checker.visit_functiondef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_docstring_lines_that_look_like_comments_2(self) -> None:
        stmt = astroid.extract_node(
            '''def f():
    """# msitake"""'''
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=2,
                args=(
                    "msitake",
                    "# msitake",
                    "  ^^^^^^^",
                    self._get_msg_suggestions("msitake"),
                ),
            )
        ):
            self.checker.visit_functiondef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_docstring_lines_that_look_like_comments_3(self) -> None:
        stmt = astroid.extract_node(
            '''def f():
    """
# msitake
    """'''
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=3,
                args=(
                    "msitake",
                    "# msitake",
                    "  ^^^^^^^",
                    self._get_msg_suggestions("msitake"),
                ),
            )
        ):
            self.checker.visit_functiondef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_docstring_lines_that_look_like_comments_4(self) -> None:
        stmt = astroid.extract_node(
            '''def f():
    """
    # cat
    """'''
        )
        with self.assertAddsMessages():
            self.checker.visit_functiondef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_docstring_lines_that_look_like_comments_5(self) -> None:
        stmt = astroid.extract_node(
            '''def f():
    """
    msitake # cat
    """'''
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=3,
                args=(
                    "msitake",
                    "    msitake # cat",
                    "    ^^^^^^^",
                    self._get_msg_suggestions("msitake"),
                ),
            )
        ):
            self.checker.visit_functiondef(stmt)

    @skip_on_missing_package_or_dict
    @set_config(spelling_dict=spell_dict)
    def test_docstring_lines_that_look_like_comments_6(self) -> None:
        stmt = astroid.extract_node(
            '''def f():
    """
    cat # msitake
    """'''
        )
        with self.assertAddsMessages(
            MessageTest(
                "wrong-spelling-in-docstring",
                line=3,
                args=(
                    "msitake",
                    "    cat # msitake",
                    "          ^^^^^^^",
                    self._get_msg_suggestions("msitake"),
                ),
            )
        ):
            self.checker.visit_functiondef(stmt)
