# Agent guidelines

## Before opening a pull request

### Check for existing work

Do this twice: before you start working on an issue, and again right before you open
your pull request. Someone may have opened one in between.

**Rule: if the issue already has an `OPEN` pull request, do not open another one.**
Review that pull request or suggest improvements on it instead. Two pull requests for
the same fix waste review time, and one of them will be closed.

#### Step 1: list the pull requests linked to the issue

On GitHub, the pull requests that will close an issue appear in the "Development" box of
the issue's sidebar. Get that list with this command. Only change `11459` to your issue
number:

```shell
gh api graphql -F number=11459 -f query='
query($number: Int!) {
  repository(owner: "pylint-dev", name: "pylint") {
    issue(number: $number) {
      closedByPullRequestsReferences(first: 50, includeClosedPrs: true) {
        nodes { number state url author { login } }
      }
    }
  }
}' --jq '.data.repository.issue.closedByPullRequestsReferences.nodes[] | "\(.state) \(.url) by \(.author.login)"'
```

Each output line is one pull request. Example output:

```text
OPEN https://github.com/pylint-dev/pylint/pull/11460 by agustin18
CLOSED https://github.com/pylint-dev/pylint/pull/11542 by aipd506
```

- A line starting with `OPEN`: someone is already working on it. Stop and follow the
  rule above.
- `MERGED`: the fix may already be on `main`. Check whether the bug still happens there.
- `CLOSED`: that attempt was abandoned. Read why before you start, so you do not repeat
  it.
- No output at all: no pull request is linked. Go to step 2.

If `gh` is not installed or not logged in, read the same data from the issue's web page.
It works without a GitHub account. Only change `11459` to your issue number:

```shell
curl -sL https://github.com/pylint-dev/pylint/issues/11459 | python3 -c '
import json, sys
page = sys.stdin.read()
key = "\"closedByPullRequestsReferences\":"
start = page.find(key)
if start == -1:
    sys.exit("Development data not found: is this an issue URL, not a pull request URL?")
data, _ = json.JSONDecoder().raw_decode(page, start + len(key))
for pr in data["nodes"]:
    print(pr["state"], pr["url"])
'
```

The output and its meaning are the same as above, without the author.

#### Step 2: search for pull requests that are not linked

Step 1 only finds pull requests that say `Closes #<number>` (or `Fixes`, `Resolves`), or
that a maintainer linked by hand. A pull request that only mentions the issue, or forgot
to mention it, is not in that list. Search for those too:

```shell
gh pr list --repo pylint-dev/pylint --state open --search "11459"
gh pr list --repo pylint-dev/pylint --state open --search "<key words from the issue title>"
```

#### Step 3: check if someone said they are working on it

List the issue's comments with their dates. Only change `11459` to your issue number:

```shell
gh issue view 11459 --repo pylint-dev/pylint --json comments --jq '.comments[] | "\(.createdAt[:10]) \(.author.login): \(.body | gsub("\n"; " ") | .[:100])"'
```

Without `gh`, read the comments on the issue's web page.

Look for a comment like "I'm working on this" or "Can I take this?". People often say
this and then never open a pull request, so a claim does not last forever:

- The claim is **active** if the person who made it did something in the last 15 days: a
  comment on the issue, or a commit or pull request for it. Do not work on the issue.
- The claim is **expired** if that person has done nothing for 15 days or more. You may
  work on the issue. Say in your pull request description that the issue was claimed by
  `@<their login>` on `<date>`, with no activity since.

### Cover every new line and branch

New and changed code in `pylint/` must be fully covered by tests: every line, and both
sides of every branch (`if`/`else`, early `return`, `and`/`or` short-circuit used as a
guard). Codecov requires 100% patch coverage. A guard that no test ever takes is either
dead code to remove or a missing test case to add.

Check it locally on the tests you touched:

```shell
pytest --cov=pylint --cov-branch --cov-report=term-missing tests/test_functional.py -k "<test name>"
```

Each new or changed line in the diff should be absent from the `Missing` column, and no
branch involving it should be listed as partial.

## AST-based checking

Pylint is an AST-based linter built on [astroid](https://github.com/pylint-dev/astroid).
When writing or modifying checkers, prefer **`isinstance` against concrete astroid node
types** combined with domain knowledge of Python syntax, rather than duck-typing with
`getattr`/`hasattr`.

The visitor pattern from `BaseChecker` already narrows the node type for you: a
`visit_call` method only receives `nodes.Call`, a `visit_assign` only receives
`nodes.Assign`, and so on. Inside such a method, the node's structure is known — its
attributes follow from the grammar (e.g. a `nodes.Call` always has `.func` and `.args`).
Walk and type-check that known structure with `isinstance` instead of probing for
attributes defensively.

Good:

```python
def visit_call(self, node: nodes.Call) -> None:
    if isinstance(node.func, nodes.Attribute):
        ...
```

Avoid:

```python
def visit_call(self, node) -> None:
    if hasattr(node.func, "attrname"):  # don't probe — check the type
        ...
```

This keeps checks precise, readable, and aligned with astroid's typed node API.

### Caveat: astroid proxies and `Uninferable`

`isinstance` checks the _static_ node type. Some astroid objects — `bases.Instance`,
`Generator`, `BoundMethod`/`UnboundMethod`, and `util.Uninferable` — resolve attributes
through `__getattr__`, proxying to a wrapped node. So `hasattr(obj, "x")` can be True at
runtime on an object whose class has no `x`, and a naive `isinstance(obj, ConcreteNode)`
will _drop_ cases the old `hasattr` caught (e.g. an exception inferred to an `Instance`
that proxies `ancestors`, or an `AsyncGenerator` that proxies `locals`).

When replacing such a guard:

- Include the proxy base in the type tuple — e.g. `(nodes.ClassDef, bases.Instance)`, or
  `(nodes.LocalsDictNodeNG, bases.Proxy)` for anything exposing `qname`.
- If the check is a behavioral _capability_ spanning heterogeneous nodes with no common
  base — or the proxied node may legitimately lack the attribute (a `BoundMethod` can
  wrap a `Lambda`, which has no `.decorators`) — keep `hasattr`. That is honest
  duck-typing, not a grammar check, and `isinstance` cannot express it safely.
