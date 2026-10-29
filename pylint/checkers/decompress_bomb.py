from __future__ import annotations

from types import NoneType
from typing import TYPE_CHECKING

from astroid import nodes
from astroid.bases import BoundMethod
from astroid.nodes import (
    Assign,
    Attribute,
    AugAssign,
    For,
    ListComp,
    NodeNG,
)

from pylint.checkers import BaseChecker, utils
from pylint.interfaces import CONTROL_FLOW, INFERENCE

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class DecompressionBombChecker(BaseChecker):

    name = "decompression-bomb"
    msgs = {
        "W5001": (
            "Unsafe decompression from the archive, %s",
            "decompression-bomb",
            "Decompressing files from non trusted sources without setting a limit "
            "on the uncompressed data's size can lead to arbitrarily large data sizes",
        ),
    }
    KNOWN_ZIP_OPENS: set[str] = {"zipfile.ZipFile", "tarfile.TarFile"}
    KNOWN_EXTRACTS: set[str] = {"zipfile.ZipFile.extract", "tarfile.TarFile.extract"}
    KNOWN_EXTRACT_ALLS: set[str] = {
        "zipfile.ZipFile.extractall",
        "tarfile.TarFile.extractall",
    }

    def eval_comp(
        self, comp: nodes.ListComp | nodes.GeneratorExp | nodes.SetComp
    ) -> str:
        iner_expr = comp.elt
        askFS = False
        if self.findVarUse("file_size", iner_expr) or self.findVarUse(
            "size", iner_expr
        ):
            askFS = True  # TODO check if it is called on the right var
        if not askFS:  # didn't check for filesize
            return "-"
        use_funcs: list[nodes.Call] = []
        if isinstance(comp.parent, nodes.Call):
            use_funcs = [comp.parent]
        elif isinstance(comp.parent, Assign):
            if comp.parent.parent:  # maybe an assert
                use_funcs = [
                    x.parent
                    for x in self.findVarUse(
                        comp.parent.targets[0].as_string(), comp.parent.parent
                    )
                    if isinstance(x.parent, nodes.Call)
                ]

        is_max = False
        is_len = False
        for fun in use_funcs:
            inferred = utils.safe_infer(fun.func)
            if isinstance(inferred, nodes.FunctionDef):
                if inferred.qname() == "builtins.sum":
                    return "FULL"
                if inferred.qname() == "builtins.max":
                    is_max = True
                elif inferred.qname() == "builtins.len":
                    is_len = True
        if is_len and is_max:
            return "FULL"
        return "MAX" if is_max else ("LEN" if is_len else "")

    def findVarUseList(
        self, varName: str, context: list[nodes.NodeNG]
    ) -> list[nodes.NodeNG]:
        return sum([self.findVarUse(varName, x) for x in context], [])

    def findVarUse(self, varName: str, context: nodes.NodeNG) -> list[nodes.NodeNG]:
        if context.as_string() == varName:
            return [context]
        attres: list[NodeNG] = []
        if isinstance(context, nodes.Attribute) and context.attrname == varName:
            attres = [context]
        return sum(
            [self.findVarUse(varName, x) for x in context.get_children()], attres
        )

    def get_file_enumerations(self, uses: list[NodeNG], kind: str) -> list[NodeNG]:
        res: list[NodeNG] = []
        if "zip" in kind:
            zipAttrs = [x.parent for x in uses if isinstance(x.parent, Attribute)]
            zipLists = [x for x in zipAttrs if x.attrname in ["filelist", "infolist"]]
            res += [
                x.parent if x.attrname == "infolist" else x
                for x in zipLists
                if x.parent
            ]
        if "tar" in kind:
            tarAttrs = [x.parent for x in uses if isinstance(x.parent, Attribute)]
            tarLists = [
                x.parent for x in tarAttrs if x.attrname == "getmembers" and x.parent
            ]
            res += uses + tarLists
        return res

    def visit_call(self, node: nodes.Call) -> None:
        infers = utils.infer_all(node.func)
        if not infers:
            return
        for inferred in infers:
            if not isinstance(inferred, BoundMethod):
                return
        if any(inferred.qname() in self.KNOWN_EXTRACT_ALLS for inferred in infers):
            self.add_message(
                "decompression-bomb",
                node=node,
                confidence=INFERENCE,
                args=("don't use extractall",),
            )
            return
        if any(inferred.qname() in self.KNOWN_EXTRACTS for inferred in infers):
            kind = ""
            if any(inferred.qname().startswith("zip") for inferred in infers):
                kind += "zip "
            if any(inferred.qname().startswith("tar") for inferred in infers):
                kind += "tar "

            ancestors: list[nodes.NodeNG] = list(node.node_ancestors())
            withNodes: list[nodes.With] = [
                x for x in ancestors if isinstance(x, nodes.With)
            ]
            possibleStarts: list[
                tuple[nodes.Call, nodes.NodeNG, list[nodes.NodeNG]]
            ] = []

            zipnameNode = node.func.last_child()
            assert zipnameNode
            zipName = ""
            if isinstance(zipnameNode, nodes.Name):
                zipName = zipnameNode.name
            elif isinstance(zipnameNode, nodes.Attribute):
                zipName = zipnameNode.as_string()  # unlikely 'ex.: self.x'
            likelyIdx = -1
            for n in withNodes:
                for gen, var in n.items:
                    if (not isinstance(gen, nodes.Call)) or isinstance(var, NoneType):
                        continue
                    infers = utils.infer_all(gen.func)
                    # inferred = utils.safe_infer(gen.func)
                    # if any((not isinstance(inferred, (nodes.ClassDef, nodes.FunctionDef)) for inferred in infers)):
                    #    continue
                    if all(
                        (not isinstance(inferred, (nodes.ClassDef, nodes.FunctionDef)))
                        or (inferred.qname() not in self.KNOWN_ZIP_OPENS)
                        for inferred in infers
                    ):
                        continue
                    if var.as_string() == zipName and likelyIdx == -1:
                        likelyIdx = len(possibleStarts)
                    possibleStarts.append((gen, var, n.body))

            if not possibleStarts:
                # TODO find a reasonable context and check there too
                return
            if -1 == likelyIdx:
                likelyIdx = len(possibleStarts) - 1

            if not zipName:
                zipName = possibleStarts[likelyIdx][1].as_string()
            zipuses = self.findVarUseList(zipName, possibleStarts[likelyIdx][2])
            archiveIters = self.get_file_enumerations(zipuses, kind)
            loops = [
                x.parent
                for x in archiveIters
                if isinstance(x.parent, For) and x.parent.iter == x
            ]
            comps = [
                x.parent
                for x in archiveIters
                if isinstance(x.parent, nodes.Comprehension) and x.parent.iter == x
            ]
            # DictCOmp has a different interface and is less practical than the others.
            coms = [
                x.parent
                for x in comps
                if isinstance(x.parent, (ListComp, nodes.GeneratorExp, nodes.SetComp))
            ]
            c = [self.eval_comp(x) for x in coms]
            uses_l = [self.findVarUseList(x.target.as_string(), x.body) for x in loops]
            fss_l = [
                [
                    y.parent
                    for y in x
                    if isinstance(y.parent, nodes.Attribute)
                    and y.parent.attrname in ["file_size", "size"]
                ]
                for x in uses_l
            ]
            is_filesize_checked = False
            is_fs_summed = False
            is_files_counted = False
            fs_summes = [
                [y for y in x if isinstance(y.parent, AugAssign)] for x in fss_l
            ]
            zipcalles = [
                x.parent for x in archiveIters if isinstance(x.parent, nodes.Call)
            ]

            if [1 for x in zipcalles if x.func.as_string() == "len"] or "LEN" in c:
                is_files_counted = True

            if sum(fs_summes, []) or "FULL" in c:
                is_fs_summed = True

            if sum(fss_l, []) or "MAX" in c:
                is_filesize_checked = True

            if is_fs_summed:
                is_filesize_checked = True
                is_files_counted = True
            msg = ""
            if not is_filesize_checked:
                msg = "filesize is not checked"
            if not is_files_counted:
                if msg:
                    msg += " "
                msg += "files are not counted"
            if (not is_filesize_checked) or (not is_files_counted):
                self.add_message(
                    "decompression-bomb",
                    node=node,
                    confidence=CONTROL_FLOW,
                    args=(msg,),
                )

    def leave_call(self, node: nodes.Call) -> None:
        pass
        # print(node)


def register(linter: PyLinter) -> None:
    linter.register_checker(DecompressionBombChecker(linter))
