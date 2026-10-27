# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests the local module directory comparison logic which requires mocking file directories."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import astroid
import pytest

from pylint.extensions import private_import
from pylint.interfaces import HIGH
from pylint.testutils import CheckerTestCase, MessageTest


class TestPrivateImport(CheckerTestCase):
    """The mocked dirname is the directory of the file being linted, the node is code inside that file."""

    CHECKER_CLASS = private_import.PrivateImportChecker

    @patch("pathlib.Path.parent")
    def test_internal_module(self, parent: MagicMock) -> None:
        parent.parts = ("", "dir", "module")
        import_from = astroid.extract_node("""from module import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("pathlib.Path.parent")
    def test_external_module_nested(self, parent: MagicMock) -> None:
        parent.parts = ("", "dir", "module", "module_files", "util")

        import_from = astroid.extract_node("""from module import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("pathlib.Path.parent")
    def test_external_module_dot_import(self, parent: MagicMock) -> None:
        parent.parts = ("", "dir", "outer", "inner", "module_files", "util")

        import_from = astroid.extract_node("""from outer.inner import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("pathlib.Path.parent")
    def test_external_module_dot_import_outer_only(self, parent: MagicMock) -> None:
        parent.parts = ("", "dir", "outer", "extensions")

        import_from = astroid.extract_node("""from outer.inner import _file""")

        with self.assertNoMessages():
            self.checker.visit_importfrom(import_from)

    @patch("pathlib.Path.parent")
    def test_external_module(self, parent: MagicMock) -> None:
        parent.parts = ("", "dir", "other")

        import_from = astroid.extract_node("""from module import _file""")

        msg = MessageTest(
            msg_id="import-private-name",
            node=import_from,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=24,
            args=("object", "_file"),
            confidence=HIGH,
        )
        with self.assertAddsMessages(msg):
            self.checker.visit_importfrom(import_from)

    @pytest.mark.parametrize("layout", ["module", "package"])
    @pytest.mark.parametrize("module_name", ["_sibling", "sibling"])
    @pytest.mark.parametrize("relative_path", [False, True])
    def test_sibling_module(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        layout: str,
        module_name: str,
        relative_path: bool,
    ) -> None:
        """Resolve siblings from the source directory without executing their code."""
        marker = tmp_path / "imported"
        content = (
            f"open({str(marker)!r}, 'w').close()\nraise RuntimeError('imported')\n"
        )
        if layout == "package":
            package = tmp_path / module_name
            package.mkdir()
            (package / "__init__.py").write_text(content, encoding="utf-8")
            (package / "child.py").write_text(content, encoding="utf-8")
            import_module = f"{module_name}.child"
        else:
            (tmp_path / f"{module_name}.py").write_text(content, encoding="utf-8")
            import_module = module_name
        if relative_path:
            monkeypatch.chdir(tmp_path)
        module = astroid.parse(
            f"from {import_module} import _private\n_private()\n",
            path="consumer.py" if relative_path else str(tmp_path / "consumer.py"),
        )

        with self.assertNoMessages():
            self.walk(module)

        assert not marker.exists()
        assert module_name not in sys.modules

    @pytest.mark.parametrize("layout", ["missing", "module", "namespace"])
    def test_nonlocal_module(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, layout: str
    ) -> None:
        """A missing module or an external dependency still warrants a warning."""
        project = tmp_path / "project"
        project.mkdir()
        module_name = "_external"
        if layout != "missing":
            dependency = tmp_path / "dependency"
            dependency.mkdir()
            if layout == "namespace":
                (dependency / "_external").mkdir()
                (dependency / "_external" / "child.py").write_text("", encoding="utf-8")
                module_name += ".child"
            else:
                (dependency / "_external.py").write_text("", encoding="utf-8")
            monkeypatch.syspath_prepend(str(dependency))
        import_line = f"from {module_name} import Public"
        module = astroid.parse(
            f"{import_line}\nPublic()\n",
            path=str(project / "consumer.py"),
        )
        import_from = module.body[0]
        msg = MessageTest(
            msg_id="import-private-name",
            node=import_from,
            args=("module", module_name),
            confidence=HIGH,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=len(import_line),
        )

        with self.assertAddsMessages(msg):
            self.walk(module)

    def test_external_namespace_portion(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A local namespace directory does not exempt its external submodules."""
        (tmp_path / "_namespace").mkdir()
        dependency = tmp_path / "dependency" / "_namespace"
        dependency.mkdir(parents=True)
        (dependency / "foreign.py").write_text("", encoding="utf-8")
        monkeypatch.syspath_prepend(str(dependency.parent))
        import_line = "from _namespace.foreign import Public"
        module = astroid.parse(import_line, path=str(tmp_path / "consumer.py"))
        msg = MessageTest(
            msg_id="import-private-name",
            node=module.body[0],
            args=("module", "_namespace.foreign"),
            confidence=HIGH,
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=len(import_line),
        )

        with self.assertAddsMessages(msg):
            self.walk(module)

    def test_type_annotations_are_collected_per_module(self) -> None:
        """The result for one module must not depend on the modules checked before it.

        https://github.com/pylint-dev/pylint/issues/11466
        """
        other = astroid.parse(
            "from pathlib import Path\nDIRECTORY = Path('.')\n", path="other.py"
        )
        annotated = astroid.parse(
            """
from _external_private.types import PublicType

def get_type() -> PublicType:
    raise NotImplementedError
""",
            path="annotated.py",
        )
        runtime = astroid.parse(
            "from _external_private.types import PublicType\nVALUE = PublicType()\n",
            path="runtime.py",
        )

        with self.assertNoMessages():
            self.walk(other)
            self.walk(annotated)

        msg = MessageTest(
            msg_id="import-private-name",
            node=runtime.body[0],
            line=1,
            col_offset=0,
            end_line=1,
            end_col_offset=46,
            args=("module", "_external_private.types"),
            confidence=HIGH,
        )
        with self.assertAddsMessages(msg):
            self.walk(runtime)
